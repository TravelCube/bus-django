from django.http import HttpResponse
from Bus import controller
import json
import logging
import time
#from celery import group

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
   # g = group(addd.s(2,2), add.s(2,3))
   # res = g.apply_async()
   # for r in res.iterate():
   #     print r
    t = time.time()
    request.session['bla'] = 'foo'
    bar = request.session.get('bla')
    #session_log(request, request.method)
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
        d = controller.get_file_names_from_bus_num(busNumber,lat,lon,acc,hour,day)
        data = [{'id':r[0], 'lastStop':r[1]} for r in d]
    except Exception as a:
	data = [{'id':0, 'lastStop':'No Bus!!!'}]
        log.exception(a)

    j = json.dumps({'data':data},ensure_ascii=False)
    #return HttpResponse(j, mimetype="text/json;charset=UTF-8")
    session_log(request, 'time: {0}'.format(time.time() - t))
    return HttpResponse(j)

def stops(request):
    if request.method == 'GET':
        file_name = str(request.GET[u'route_id'])
    else:
        file_name = str(request.POST[u'route_id'])
    session_log(request, 'args: {0}'.format(file_name))
    stopsl = bus.get_stops(file_name)
    if stopsl == None:
        #return error
        pass
    data = [{'name':x[1], 'order':0, 'id':x[0], 'lat':x[3], 'lon':x[4]} for x in stopsl]
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

