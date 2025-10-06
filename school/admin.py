from django.contrib import admin     
from .models import Category, Course, Teacher


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")  
    search_fields = ("name", "slug")               
    list_per_page = 20


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("first_name", "is_active", "created_at")  
    list_filter = ("is_active",)
    search_fields = ("first_name",)
    list_per_page = 20


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "is_active", "created_at")  
    list_filter = ("category", "level", "is_active", "created_at")
    search_fields = ("title", "teacher__first_name")  
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"   
    ordering = ("-created_at",)
    list_per_page = 25
