from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def role_required(*allowed_roles):
    def decorator(view_func):
        def check_role(user):
            if not user.is_authenticated:
                return False

            if hasattr(user, 'role') and user.role in allowed_roles:
                return True

            return False

        return user_passes_test(check_role, login_url='users:login')(view_func)
    return decorator