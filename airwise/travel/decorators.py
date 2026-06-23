from django.shortcuts import redirect
from functools import wraps

def connexion_requise(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('utilisateur_id'):
            return redirect('connection')
        return view_func(request, *args, **kwargs)
    return _wrapped_view