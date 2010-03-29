from django.conf.urls.defaults import *



urlpatterns = patterns('',
    
    (r'^$', 'urly.urly_app.views.index'),
    (r'^urly/get/$', 'urly.urly_app.views.get'),
    (r'^urly/popular/$', 'urly.urly_app.views.popular'),
    (r'^urly/latest/$', 'urly.urly_app.views.latest'),
    (r'^urly/random/$', 'urly.urly_app.views.random'),
    (r'^(?P<key>\w+)/$', 'urly.urly_app.views.request_url'),
    
    
    
    

)
