from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Category, Course


@receiver(pre_save, sender=Category)
def fill_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)   


@receiver(pre_save, sender=Course)
def fill_course_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)