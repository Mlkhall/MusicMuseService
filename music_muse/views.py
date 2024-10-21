from django.http import HttpResponse, HttpRequest
from django.template import loader


def index(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))
