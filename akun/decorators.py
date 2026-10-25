from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def peran_wajib(*daftar_peran):
    """Dekorator kontrol akses berbasis peran (NFR-02)."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("masuk")
            if request.user.peran not in daftar_peran:
                raise PermissionDenied("Anda tidak memiliki hak akses ke halaman ini (HTTP 403).")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator