from django.http import HttpResponse
from Bus import bus
import json

def lines(request):
    q = request.POST
    names,r = bus.get(1,2,3,4,5)
    data = [{'id':key, 'lastStop':value} for key,value in names]
    request.session['lines'] = r
    j = json.dumps({'data':data},ensure_ascii=False)
    #return HttpResponse(j, mimetype="text/json;charset=UTF-8")
    return HttpResponse(j)

def stops(request):
    route_id = int(request.POST[u'route_id'])
    l = request.session['lines']
    res = [x[1] for x in l if x[0] == route_id]
    stops = bus.get_stops(res)
    if stops == None:
        #return error
        pass
    data = [{'name':x[4], 'order':x[3], 'id':x[2], 'lat':31.1, 'lon':32.2} for x in stops]
    j = json.dumps({'data':data},ensure_ascii=False)
    return HttpResponse(j)

