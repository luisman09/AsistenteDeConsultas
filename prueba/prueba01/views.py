#from django.http import HttpResponse							#1,2,3
#from django.template import RequestContext, loader				#3
#from django.http import Http404								#4


from .models import Estado, Municipio

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


def edo(request):
    #return HttpResponse("Hello, world.")						#1
    estado_list = Estado.objects.order_by('nombre')[:25]		#2,3,4
    #output = ', '.join([p.nombre for p in estado_list])		#2
    #return HttpResponse(output)								#2
    #template = loader.get_template('prueba01/index.html')		#3
    #context = RequestContext(request, {						#3
    #    'estado_list': estado_list,							#3
    #})															#3	
    #return HttpResponse(template.render(context))				#3
    context = {'estado_list': estado_list}						#4
    return render(request, 'prueba01/edo.html', context)		#4


def mun(request, estado):
    #return HttpResponse("Estado %s." % estado)							#1,2
    edo = get_object_or_404(Estado, pk=estado)
    return render(request, 'prueba01/mun.html', {'edo': edo})

''' #Vistas genericas
class EdoView(generic.ListView):
    template_name = 'prueba01/edo.html'
    context_object_name = 'estado_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Estado.objects.order_by('nombre')[:25]


class MunView(generic.DetailView):
    model = Estado
    template_name = 'prueba01/mun.html'
'''



