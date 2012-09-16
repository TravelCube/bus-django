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

def lines(request):
    t = time.time()
    log.info(request.method)
    if request.method == 'GET':
        busNumber = str(request.GET[u'bus'])
        lat = str(request.GET[u'lat'])
        lon = str(request.GET[u'lon'])
        acc = str(request.GET[u'acc'])
        hour = str(request.GET[u'hour'])
        hour = hour + ':00:00'
        day = request.GET[u'day']
        day = days[int(str(day))]
    else:
        busNumber = request.POST[u'bus']
        lat = request.POST[u'lat']
        lon = request.POST[u'lon']
        acc = request.POST[u'acc']
        hour = request.POST[u'hour']
        hour = hour + ':00:00'
        day = request.POST[u'day']
        day = days[int(str(day))]

    log.info('args: {0}'.format((busNumber,lat,lon,acc,hour,day)))

    try:
        names,r = bus.get(busNumber,lat,lon,acc,hour,day)
    except Exception as a:
        log.exception(a)

    data = [{'id':key, 'lastStop':value} for key,value in names]
    request.session['lines'] = r
    j = json.dumps({'data':data},ensure_ascii=False)
    #return HttpResponse(j, mimetype="text/json;charset=UTF-8")
    log.info('time: {0}'.format(time.time() - t))
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
    log.info('user {0}, {1}'.format(request.session.session_key, choice))
    return HttpResponse('ok')

