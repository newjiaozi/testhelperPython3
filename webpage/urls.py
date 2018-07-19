
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.handlePage,name='mainPage'),
    url(r'^createPlan/$',views.createPlan,name='createPlan'),
    url(r'^checkPlan/$',views.checkPlan,name='checkPlan'),
    url(r'^changeMoney/$',views.changeMoney,name='changeMoney'),
    url(r'^codisFlush/$',views.codisFlush,name='codisFlush'),
    url(r'^jsonFormat/$',views.jsonFormat,name='jsonFormat'),
    url(r'^timesTamp/$',views.timesTamp,name='timesTamp'),
    url(r'^base64Image/$',views.base64Image,name='base64Image'),
    url(r'^imageBase64/$',views.imageBase64,name='imageBase64'),
    url(r'^interfaceTest/$',views.interfaceTest,name='interfaceTest'),
    url(r'^params2Dict/$',views.params2Dict,name='params2Dict'),
    url(r'^getRateUuid/$',views.getRateUuid,name='getRateUuid'),

]
