from django.shortcuts import redirect

def admin_control(url_mapping):
    def wrapper(*args, **kwargs):
        request = args[1]
        request_path = request.get_full_path()
        session = request.session
        admin = session.get('admin')
        if admin is None:
            return redirect('/admin/login?next='+request_path)
        return url_mapping(*args, **kwargs)

    return wrapper
