# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response

def homepage(request):
	return render_to_response('homepage.html', context_instance=RequestContext(request))
