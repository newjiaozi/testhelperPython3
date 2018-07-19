#coding:utf-8

"""TestHelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import time,os,logging


today = time.strftime("%Y-%m-%d",time.localtime())
par_dir =  os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
log_dir = os.path.join(par_dir,"logs")
 
logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt = '%a, %d %b %Y %H:%M:%S',  
                    filename = os.path.join(log_dir,"%s.txt" % today),
                    filemode = 'w+') 

console = logging.StreamHandler()  
console.setLevel(logging.INFO)  

formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')  
console.setFormatter(formatter)  

logging.getLogger('').addHandler(console)  







urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^web/', include('webpage.urls')),
    url(r'^resp/', include('resp.urls')),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),  
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), 
]
