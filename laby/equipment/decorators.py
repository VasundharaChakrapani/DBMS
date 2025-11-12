from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        return redirect('no_permission')
    return _wrapped_view

def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['Admin', 'Staff']:
            return view_func(request, *args, **kwargs)
        return redirect('no_permission')
    return _wrapped_view

def viewer_allowed(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # all logged-in users (Admin, Staff, Viewer) can see
        return view_func(request, *args, **kwargs)
    return _wrapped_view
