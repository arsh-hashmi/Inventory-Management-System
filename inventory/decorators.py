from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    """Decorator that checks if the logged-in user has the ADMIN role.

    Redirects to the dashboard with an error message if the user is not an admin.
    Must be used *after* @login_required so that request.user is authenticated.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('inventory:dashboard')
        return view_func(request, *args, **kwargs)

    return _wrapped
