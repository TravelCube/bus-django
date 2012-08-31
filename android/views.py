from django.http import HttpResponse
from Bus import bus

def lines(request):
    q = request.GET
    names = bus.get(1,2,3,4,5)
    return HttpResponse(names[0])

