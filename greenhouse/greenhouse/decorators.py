from django.shortcuts import render

def login_necessary():
    def decorator(func):
        def wrap(request, *args, **kwargs):
            if not request.session.get('uid', None):
                return render(request, 'Login.html')
            else:
                return func(request, *args, **kwargs)
        return wrap
    return decorator