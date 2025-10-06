from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from school.models import Course

class Command(BaseCommand):
    help = "Guruhlar va ruxsatlar yaratadi"

    def handle(self, *args, **options):
        ct = ContentType.objects.get_for_model(Course)

        # xavfsizroq usul: barcha ruxsatlarni bir martada olamiz va keyin tekshiramiz
        expected = ["add_course", "change_course", "delete_course", "view_course"]
        perms_qs = Permission.objects.filter(content_type=ct, codename__in=expected)
        perms = {p.codename: p for p in perms_qs}

        missing = set(expected) - set(perms.keys())
        if missing:
            self.stderr.write(self.style.ERROR(
                f"Quyidagi ruxsatlar topilmadi: {', '.join(missing)}. "
                "Avval migrations qiling va app INSTALLED_APPS ga qo'shilganiga ishonch hosil qiling."
            ))
            return

        manager, _ = Group.objects.get_or_create(name="manager")
        manager.permissions.set([
            perms["add_course"],
            perms["change_course"],
            perms["delete_course"],
            perms["view_course"],
        ])

        teacher, _ = Group.objects.get_or_create(name="teacher")
        teacher.permissions.set([perms["view_course"]])

        self.stdout.write(self.style.SUCCESS("Guruhlar va ruxsatlar yaratildi"))
