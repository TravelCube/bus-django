from django.http import HttpResponse
from Bus import bus
import json

def lines(request):
    q = request.GET
    names = bus.get(1,2,3,4,5)
    data = [{'id':key, 'lastStop':value} for key,value in names.items()]
    j = json.dumps({'data':data},ensure_ascii=False)
    #return HttpResponse(j, mimetype="text/json;charset=UTF-8")
    return HttpResponse(j)

