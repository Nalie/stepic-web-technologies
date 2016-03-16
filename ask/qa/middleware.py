from django.utils import timezone

from models import Session


class CheckSessionMiddleware(object):
    def process_request(request):
        print 'process_request'
        try:
            sessid = request.COOKIE.get('sessid')
            print sessid
            session = Session.objects.get(
                key=sessid,
                expires__gt=timezone.now(),
            )
            print session.user
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            print 'session doesnt exist'
            request.session = None
            request.user = None