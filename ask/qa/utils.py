from datetime import timedelta
from django.utils import timezone


def get_hexdigest(salt, password):
    import hashlib
    return hashlib.sha1('%s%s' % (salt, password)).hexdigest()


def make_password(raw_password):
    import random
    salt = get_hexdigest(str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s' % (salt, hsh)


def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(salt, raw_password)


def generate_session_id():
    import uuid
    return uuid.uuid1()


def do_login(login, password):
    # from models import User, Session
    from django.contrib.auth.models import User
    from django.contrib.sessions.models import Session
    from django.contrib.auth import authenticate
    user = authenticate(username=login, password=password)
    if user is not None:
    # the password verified for the user
        if user.is_active:
            return True
    return False
    # try:
    #     user = User.objects.get(username=login)
    # except User.DoesNotExist:
    #     return None
    # if not check_password(password, user.password):
    #     return None
    # key = generate_session_id()
    # session = Session.objects.create(key=key, expires=timezone.now() + timedelta(days=5), user=user)
    # return session
