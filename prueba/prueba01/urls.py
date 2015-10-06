from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.edo, name='edo'),									# no generico
    url(r'^(?P<estado>[0-9]+)/$', views.mun, name='mun'),				# no generico
	#url(r'^$', views.EdoView.as_view(), name='edo'),
    #url(r'^(?P<pk>[0-9]+)/$', views.MunView.as_view(), name='mun'),
]
