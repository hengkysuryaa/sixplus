from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):        
            group = None
            # print(request.user.groups.all())
            # print(allowed_roles)
            if request.user.groups.exists():
                groups = request.user.groups.all()
            
            for group in groups:
                # print(group)
                for role in allowed_roles:
                    # print(role)
                    if group.name == role:
                        return view_func(request, *args, **kwargs)
                    
            return HttpResponse("Anda tidak memiliki izin untuk laman ini")

        return wrapper_func
    return decorator