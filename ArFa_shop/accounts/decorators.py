from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def check_position(allowed_positions, redirect_url='/accounts/login/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.position in allowed_positions:
                return view_func(request, *args, **kwargs)
            else:
                # هدایت به صفحه مشخص به جای خطای 403
                return redirect(redirect_url)
        return _wrapped_view
    return decorator
