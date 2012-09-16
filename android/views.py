from django.http import HttpResponse
from Bus import bus
import json
import logging
import time

log = logging.getLogger('android')

days = {}
days[1] = 'sunday'
days[2] = 'monday'
days[3] = 'tuesday'
days[4] = 'wednesday'
days[5] = 'thursday'
days[6] = 'friday'
days[7] = 'saturday'

def get_parms(request):
    if request.method == 'GET':
        return request.GET
    elif request.method == 'POST':
        return request.POST

def lines(request):
    t = time.time()
    log.info(request.method)
    session_log(request, request.method)
    parms = get_parms(request)
    busNumber = str(parms[u'bus'])
    lat = str(parms[u'lat'])
    lon = str(parms[u'lon'])
    acc = str(parms[u'acc'])
    hour = str(parms[u'hour'])
    hour = hour + ':00:00'
    day = parms[u'day']
    day = days[int(str(day))]

    session_log(request, 'args: {0}'.format((busNumber,lat,lon,acc,hour,day)))

    try:
        names,r = bus.get(busNumber,lat,lon,acc,hour,day)
    except Exception as a:
        log.exception(a)

    data = [{'id':key, 'lastStop':value} for key,value in names]
    request.session['lines'] = r
    j = json.dumps({'data':data},ensure_ascii=False)
    #return HttpResponse(j, mimetype="text/json;charset=UTF-8")
    session_log(request, 'time: {0}'.format(time.time() - t))
    return HttpResponse(j)

def stops(request):
    if request.method == 'GET':
        route_id = int(request.GET[u'route_id'])
    else:
        route_id = int(request.POST[u'route_id'])
    l = request.session['lines']
    res = [x[1] for x in l if x[0] == route_id]
    stopsl = bus.get_stops(res)
    if stopsl == None:
        #return error
        pass
    data = [{'name':x[4], 'order':x[3], 'id':x[2], 'lat':x[7], 'lon':x[8]} for x in stopsl]
    j = json.dumps({'data':data},ensure_ascii=False)
    return HttpResponse(j)


def userop(request):
    if request.method == 'GET':
        choice = int(request.GET[u'choice'])
    else:
        choice = int(request.POST[u'choice'])
    session_log(request, choice)
    return HttpResponse('ok')

def client_log(request):
    session_log(request, get_parms(request)[u'log'])
    return HttpResponse('ok')

def alert(request):
    parms = get_parms(request)
    msg = 'lat: {0}, lon: {1}, acc: {2}'.format(parms[u'lat'], parms[u'lon'], parms[u'acc'])
    session_log(request, msg)
    return HttpResponse('ok')

def session_log(request, msg):
    log.info('user {0}, {1}'.format(request.session.session_key, msg))

