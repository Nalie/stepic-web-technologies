from django.utils import timezone

from models import Session


class CheckSessionMiddleware(object):
    def process_request(request):
        try:
            sessid = request.COOKIE.get('sessid')
            session = Session.objects.get(
                key=sessid,
                expires__gt=timezone.now(),
            )
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None
