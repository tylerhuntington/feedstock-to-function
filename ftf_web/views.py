from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

def redirect(request, **kwargs):
    hostname = request.get_host().split(':')[0]
    return HttpResponseRedirect(f"https://{hostname}:{kwargs.get('var')}")

class HomePageView(TemplateView):
    template_name = 'home.html'



