from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = ['boss', 'manager']

    def test_func(self):
        user = self.request.user
        if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False):
            return True
        
        role = getattr(user, 'position', None)
        return role in self.allowed_roles