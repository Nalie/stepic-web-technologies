from django.utils import timezone

from models import Session


class CheckSessionMiddleware(object):

    def process_request(self, request):
        try:
            sessid = request.COOKIES.get('session')
            if sessid is not None:
                session = Session.objects.get(
                    key=sessid,
                    expires__gt=timezone.now(),
                )
                request.session = session
                request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None

    def process_response(self, request, response):
        try:
            print 'response: ' + response
            print 'response.cookies: ' + response.cookies
        except Exception:
            print 'hz'
        finally:
            return response

    def process_exception(self, request, exception):
        print exception