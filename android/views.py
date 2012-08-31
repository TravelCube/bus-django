from django.http import HttpResponse

def lines(request):
    q = request.GET
    return HttpResponse(q.items())

