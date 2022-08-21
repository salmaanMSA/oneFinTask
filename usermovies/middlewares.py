from django.utils.deprecation import MiddlewareMixin
from .models import RequestCounter


class RequestCounterMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super().__init__(get_response)

    def __call__(self, request):
        response = self.get_response(request)
        try:
            # get request counter obj
            counter = RequestCounter.objects.get()
            counter.no_of_request += 1  # increment by 1
            counter.save()

        except RequestCounter.DoesNotExist:
            # create new request counter obj
            req_cnt = RequestCounter.objects.create(no_of_request=1)

        return response
