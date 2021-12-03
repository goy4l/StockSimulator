
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import lauth
from simulator import views 
from django.contrib.auth.decorators import login_required


class lauthMiddleware(MiddlewareMixin):

    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):

        # Code that is executed in each request before the view is called
        response = self.get_response(request)

        # Code that is executed in each request after the view is called
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # This code is executed just before the view is called
       if request.user.is_authenticated:
        if not lauth.objects.filter(user=request.user).exists() and not view_func == views.Lauth:
          return HttpResponse("<meta http-equiv='refresh' content='0; URL=/lauth' />")
       #print('helo')
    def process_exception(self, request, exception):
        # This code is executed if an exception is raised
        print(exception)

    def process_template_response(self, request, response):
        # This code is executed if the response contains a render() method
        return response