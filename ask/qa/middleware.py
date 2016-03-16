from django.utils import timezone

from models import Session


class CheckSessionMiddleware(object):

    def process_request(self, request):
        print request
        print request.get_signed_cookie('sessid', 'ttt')
        try:
            sessid = request.get_signed_cookie('sessid', '')
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
        except Exception:
            print 'hz'
        return request
