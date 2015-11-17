from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^atributos/$', login_required(views.AtributosView.as_view()), name='atributos'),
    url(r'^consultas/$', login_required(views.consultas), name='consultas'),
    url(r'^queries/$', login_required(views.QueriesView.as_view()), name='queries'),
    url(r'^consultas_queries/$', login_required(views.consultas_queries), name='consultas_queries'),
    url(r'^muestras/$', login_required(views.MuestrasView.as_view()), name='muestras'),
    url(r'^consultas_muestras/$', login_required(views.consultas_muestras), name='consultas_muestras'),
    url(r'^busqueda_ajax/$', login_required(views.BusquedaAjaxView.as_view()), name='busqueda_ajax'),
    url(r'^busqueda_ajax2/$', login_required(views.BusquedaAjax2View.as_view()), name='busqueda_ajax2'),
    url(r'^busqueda_ajax3/$', login_required(views.BusquedaAjax3View.as_view()), name='busqueda_ajax3'),
    url(r'^busqueda_ajax4/$', login_required(views.BusquedaAjax4View.as_view()), name='busqueda_ajax4'),
    url(r'^buscar_centro/$', login_required(views.BuscarCentroAjaxView.as_view()), name='buscar_centro'),
    url(r'^limpiar_globales/$', login_required(views.limpiarGlobales), name='limpiar_globales'),
    url(r'^exportar_csv/$', login_required(views.exportar_csv), name='exportar_csv'),
    #url(r'^generar_matriz/$', login_required(views.GenerarMatrizAjaxView.as_view()), name='generar_matriz'),

]


