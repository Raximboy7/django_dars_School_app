from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.validators import RegexValidator, MinLengthValidator

# Boshlang‘ich darajalar
LEVEL_CHOICES = [
    ('beg', 'Beginner'),
    ('int', 'Intermediate'),
    ('adv', 'Advanced'),
]


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message="Telefon raqami faqat raqam bo‘lsin (+998901234567 ko‘rinishida)."
)


# Category model
class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name = "Kategoriya"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def _generate_unique_slug(self):
        base = slugify(self.name)
        slug = base
        i = 1
        # exclude(self.pk) so that updating the same instance won't collide with itself
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


# Teacher model
class Teacher(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to='teachers/', blank=True, null=True,
        help_text="300x300 px tavsiya etiladi"
    )
    telegram = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        # agar last_name bo'lmasa faqat first_name qaytarsin
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


# Course model
class Course(TimeStampedModel):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="courses"
    )
    title = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='beg')
    duration_months = models.PositiveSmallIntegerField(default=3)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_students = models.PositiveSmallIntegerField(default=20)
    is_online = models.BooleanField(default=False)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "category"], name="unique_course_per_category")
        ]

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        base = slugify(self.title)
        slug = base
        i = 1
        while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def clean(self):
        # chaqirishni qo'shdim, shunda super klassning ham validatsiyalari ishlaydi
        super().clean()

        # Decimal bilan aniq solishtirish uchun Decimal('0')
        if Decimal(self.price) < Decimal('0'):
            raise ValidationError("Narx manfiy bo'lishi mumkin emas.")
        if self.max_students <= 0:
            raise ValidationError("Guruh hajmi 0 dan katta bo'lishi kerak.")
        if self.is_online and self.max_students > 60:
            raise ValidationError("Onlayn kurslar uchun maksimal o'quvchilar soni 60 oshmasligi kerak.")
        if self.teacher and not getattr(self.teacher, 'is_active', True):
            raise ValidationError("Faol bo'lmagan o‘qituvchi biriktirilmasin.")

    def save(self, *args, **kwargs):
        # slug bo'sh bo'lsa, unik slug yaratamiz
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # url nomini loyihangizdagi urls.py ga moslang (misol: 'school:course_detail')
        return reverse('school:course_detail', kwargs={'slug': self.slug})
