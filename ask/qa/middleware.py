from django.utils import timezone

from models import Session


class CheckSessionMiddleware(object):

    def process_request(self, request):
        try:
            sessid = request.get_signed_cookie('sessid', '')
            session = Session.objects.get(
                key=sessid,
                expires__gt=timezone.now(),
            )
            request.session = session
            request.user = session.user
            print request
            print session
        except Session.DoesNotExist:
            request.session = None
            request.user = None
