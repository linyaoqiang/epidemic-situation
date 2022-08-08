from django.shortcuts import redirect


def user_control(url_mapping):
    def wrapper(*args, **kwargs):
        request = args[1]
        request_path = request.get_full_path()
        session = request.session
        admin = session.get('user')
        if admin is None:
            return redirect('/login')
        return url_mapping(*args, **kwargs)

    return wrapper
