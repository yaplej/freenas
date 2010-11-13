#+
# Copyright 2010 iXsystems
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# $FreeBSD$
#####################################################################

from freenasUI.network.forms import * 
from freenasUI.network.models import * 
from freenasUI.network.views import * 
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import Http404
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import update_object, delete_object
from freenasUI.middleware.notifier import notifier
import os, commands

## Network Section

@login_required
def network(request, objtype = None):
    gc = GlobalConfigurationForm(data = GlobalConfiguration.objects.order_by("-id").values()[0])
    interfaces = InterfacesForm()
    vlan = VLANForm()
    lagg = LAGGForm()
    staticroute = StaticRouteForm()
    int_list = Interfaces.objects.order_by("-id").values()
    vlan_list = VLAN.objects.order_by("-id").values()
    lagg_list = LAGG.objects.order_by("-id").values()
    sr_list = StaticRoute.objects.order_by("-id").values()
    if request.method == 'POST':
        if objtype == 'configuration':
            gc = GlobalConfigurationForm(request.POST)
            if gc.is_valid():
                gc.save()
                return HttpResponseRedirect('/network/')
        elif objtype == 'int':
            interfaces = InterfacesForm(request.POST)
            if interfaces.is_valid():
                interfaces.save()
                return HttpResponseRedirect('/network/')
        elif objtype == 'vlan':
            vlan = VLANForm(request.POST)
            if vlan.is_valid():
                vlan.save()
                return HttpResponseRedirect('/network/')
        elif objtype == 'lagg':
            lagg = LAGGForm(request.POST)
            if lagg.is_valid():
                lagg.save()
                return HttpResponseRedirect('/network/')
        elif objtype == 'sr':
            staticroute = StaticRouteForm(request.POST)
            if staticroute.is_valid():
                staticroute.save()
        else:
            raise Http404() 
    variables = RequestContext(request, {
        'gc': gc,
        'interfaces': interfaces,
        'vlan': vlan,
        'lagg': lagg,
        'staticroute': staticroute,
        'int_list': int_list,
        'vlan_list': vlan_list,
        'lagg_list': lagg_list,
        'sr_list': sr_list,
    })
    return render_to_response('network/index.html', variables)

@login_required
def generic_delete(request, object_id, model_name):
    network_name_model_map = {
        'interfaces':    Interfaces,
        'staticroute':   StaticRoute,
        'lagg':   LAGG,
        'vlan':   VLAN,
    }
    return delete_object(
        request = request,
        model = network_name_model_map[model_name],
        post_delete_redirect = '/network/',
        object_id = object_id, )

@login_required
def generic_update(request, object_id, model_name):
    model_name_to_model_and_form_map = {
            'interfaces':   ( Interfaces, None ),
            'vlan':   ( VLAN, None ),
            'lagg':   ( LAGG, None ),
            'staticroute':   ( StaticRoute, None ),
            } 
    model, form_class = model_name_to_model_and_form_map[model_name]
    return update_object(
        request = request,
        model = model, form_class = form_class,
        object_id = object_id, 
        post_save_redirect = '/network/',
        )

