from datetime import timedelta, datetime


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
    print raw_password
    print enc_password
    print hsh
    print get_hexdigest(salt, raw_password)
    return hsh == get_hexdigest(salt, raw_password)


def generate_session_id():
    import uuid
    print 'generate ses id'
    return uuid.uuid1()


def do_login(login, password):
    from models import User, Session
    try:
        user = User.objects.get(username=login)
    except User.DoesNotExist:
        return None
    if not check_password(password, user.password):
        return None
    print 'session start created'
    key = generate_session_id()
    print key
    session = Session(key=key, user=user, expires=datetime.now() + timedelta(days=5))
    print session
    session.save()
    print session
    return session
