from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    #url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    #url(r'^(?P<pk>[0-9]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^atributos/$', login_required(views.AtributosView.as_view()), name='atributos'),
    #url(r'^(?P<parroquia_id>[0-9]+)/vote/$', login_required(views.vote), name='vote'),
    url(r'^consultas/$', login_required(views.consultas), name='consultas'),
    url(r'^queries/$', login_required(views.queries), name='queries'),
    url(r'^busqueda_ajax/$', login_required(views.BusquedaAjaxView.as_view()), name='busqueda_ajax'),
    url(r'^busqueda_ajax2/$', login_required(views.BusquedaAjax2View.as_view()), name='busqueda_ajax2'),
    url(r'^busqueda_ajax3/$', login_required(views.BusquedaAjax3View.as_view()), name='busqueda_ajax3'),
    url(r'^buscar_centro/$', login_required(views.BuscarCentroAjaxView.as_view()), name='buscar_centro'),
]


