from django.shortcuts import render
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin

from .mixins import StaffRequiredMixin
from .models import Course, Category, Teacher
from .forms import CourseForm


# --- Oddiy sahifalar ---
def home(request):
    ctx = {
        'title': 'Bosh sahifa',
        'hero': 'Xush kelibsiz!',
        'headline': "Django o'rganishni bugun boshlang!",
        'sub': '1-haftada - MVT, shablonlar, static, URLlar',
        'cta_text': 'Kursni davom ettirish',
        'cta_url': '/about/',
    }
    return render(request, 'home.html', ctx)


def about(request):
    return render(request, 'about.html', {'title': 'Biz haqimizda'})


# --- Slug generatsiya qilish ---
@receiver(pre_save, sender=Category)
def fill_category_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Course)
def fill_course_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


# --- Kurslar bilan ishlash ---
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 9

    def get_queryset(self):
        qs = (
            Course.objects
            .select_related('category', 'teacher')
            .filter(is_active=True)
        )

        q = self.request.GET.get('q', '').strip()
        cat = self.request.GET.get('cat', '').strip()
        lvl = self.request.GET.get('lvl', '').strip()
        tch = self.request.GET.get('tch', '').strip()
        onl = self.request.GET.get('onl', '').strip()
        order = self.request.GET.get('o', '').strip()

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(teacher__first_name__icontains=q) |
                Q(teacher__last_name__icontains=q)
            )
        if cat:
            qs = qs.filter(category_id=cat)
        if lvl:
            qs = qs.filter(level=lvl)
        if tch:
            qs = qs.filter(teacher_id=tch)
        if onl == '1':
            qs = qs.filter(is_online=True)

        if order:
            if order == 'new':
                qs = qs.order_by('-id')
            else:
                qs = qs.order_by(order)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Kurslar"
        ctx['categories'] = Category.objects.order_by('name')
        ctx['teachers'] = Teacher.objects.filter(is_active=True).order_by('first_name', 'last_name')
        ctx['current'] = {
            'q': self.request.GET.get('q', '').strip(),
            'cat': self.request.GET.get('cat', '').strip(),
            'lvl': self.request.GET.get('lvl', '').strip(),
            'tch': self.request.GET.get('tch', '').strip(),
            'onl': self.request.GET.get('onl', '').strip(),
            'o': self.request.GET.get('o', '').strip(),
        }
        ctx['add_url'] = reverse_lazy('school:course_add')
        return ctx


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class CourseUpdateView(StaffRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = "Kurs muvaffaqiyatli yangilandi!"
    permission_required = 'school.change_course'   # <-- qo'shildi

    def get_success_url(self):
        return self.object.get_absolute_url()


class CourseDeleteView(StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy("school:course_list")
    permission_required = 'school.delete_course'   # <-- qo'shildi


class CourseCreateView(StaffRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_message = "Kurs muvaffaqiyatli qo‘shildi!"
    permission_required = 'school.add_course'     # <-- qo'shildi

    def get_success_url(self):
        return reverse_lazy("school:course_list")
