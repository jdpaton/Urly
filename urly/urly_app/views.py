from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from urly.urly_app.models import Urly
from django.conf import settings

def index(request):
  
    t = loader.get_template('index.html')
    c = RequestContext(request,{
        'page': '1',
    })
    return HttpResponse(t.render(c))
    
def get(request):
  
  if not request.POST['url']:
    return error(request)
    
  from datetime import datetime
  
  key = None
  ret_val = None
  
  url = request.POST['url']
  
  #check url
  import urlparse
  pieces = urlparse.urlparse(url)
  
  if not pieces.scheme:
    url = 'http://' + url
    
  
  
  if Urly.objects.filter(url = url ).count() > 0:
    
    urly = Urly.objects.get(url = url)
    key = urly.key
    
    ret_val = settings.SERVER_NAME + key

      
  else:
    u = Urly()
    key = u.get_new_key()
    
    u.expired = False
    u.url = url
    u.hits = 0
    u.request_ip = request.META['REMOTE_ADDR']
    u.last_hit = datetime.now()
    u.key = key
    u.private = False
    
    u.save()
      
    ret_val = settings.SERVER_NAME + key
  
  return HttpResponse('<a href="%s">%s</a>' % (ret_val, ret_val))



  
def request_url(request, key):
  
  try:
    urly = Urly.objects.get(key=key)
    urly.hits = urly.hits + 1
    urly.save()
    
    return HttpResponseRedirect(urly.url)
    
  except Urly.DoesNotExist:
    return error(request)
  
  
def error(request):
  return HttpResponse("err")
  
def popular(request):
  
  urlies = Urly.objects.filter(hits__gte=1, private=False)[0:3]
  
  if urlies:
    from django.core import serializers
    data = serializers.serialize("json", urlies)
    return HttpResponse(data, mimetype='application/json')
  else:
    return HttpResponse('{}', mimetype='application/json')
    
def latest(request):
  
  urlies = Urly.objects.filter(private=False)[0:3]

  if urlies:
    from django.core import serializers
    data = serializers.serialize("json", urlies)
    return HttpResponse(data, mimetype='application/json')
  else:
    return HttpResponse('{}', mimetype='application/json')
    
def random(request):
  
  urlies_count = Urly.objects.count()
  
  if urlies_count:
    
    from random import sample

    max_rows = 3
     
    rand_nums = sample(xrange(1,urlies_count), 2)

    # Match ID's of pictures to the sampled list
    random_urlies = Urly.objects.filter(id__in = rand_nums)[:max_rows]

    from django.core import serializers
    data = serializers.serialize("json", random_urlies)
    return HttpResponse(data, mimetype='application/json')
    
    
  

    
  
