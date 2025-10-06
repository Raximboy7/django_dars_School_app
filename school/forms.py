from django import forms
from .models import Course, Teacher, Category


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'category',
            'title',
            'level',
            'duration_months',
            'price',
            'max_students',
            'is_online',
            'teacher',
            'is_active',
            'slug'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Masalan: Python Asoslari'}),
            'duration_months': forms.NumberInput(attrs={'min': 1, 'max': 24}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'max_students': forms.NumberInput(attrs={'min': 1, 'max': 50}),
        }
        help_texts = {
            'slug': "Ixtiyoriy. Bo'sh qoldirsangiz avtomatik hosil bo'ladi."
        }

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)

        # Bootstrap klasslarini qo‘shib chiqamiz
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        # Faqat aktiv teacher’larni chiqarish
        self.fields['teacher'].queryset = Teacher.objects.filter(is_active=True).order_by('full_name')
        self.fields['category'].queryset = Category.objects.order_by('name')

    def clean_price(self):
        p = self.cleaned_data.get('price')
        if p is not None and p < 0:
            raise forms.ValidationError("Narx manfiy bo'lishi mumkin emas.")
        return p

    def clean_max_students(self):
        m = self.cleaned_data.get('max_students')
        if m is not None and m < 0:
            raise forms.ValidationError("Talabalar soni manfiy bo'lishi mumkin emas.")
        return m