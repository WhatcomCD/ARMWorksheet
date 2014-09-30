#
#  django imports
#
from django.conf import settings
from django.forms import Form
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView


#
#  sys imports
#
import json
from os import path
import logging
logger = logging.getLogger( __file__ )


#
#  app imports
#
from common.functions.filesystem import create_dirs


class WorksheetForm( Form ):

    def __init__( self, *args, **kwargs ):
        super( WorksheetForm, self ).__init__( *args, **kwargs )

    def clean( self ):
        cleaned_data = super( WorksheetForm, self ).clean()
        return cleaned_data


class WorksheetView( FormView ):

    template_name = 'worksheet.html'
    form_class = WorksheetForm 

    http_method_names = [ 'get', 'post', ]

    def get( self, request, *args, **kwargs ):

        data = {
                'page_name': 'ARM Worksheet',
        }
        data.update( csrf( request ) )

        return render_to_response( self.template_name, data )

    def set_success_url( self ):
        self.success_url = reverse( 'arm:ThanksVi', kwargs = { 'client_id' : client.client_id } )

    def form_valid( self, form ):
        pass


    def form_invalid(self, form):
        pass

    def post( self, request, *args, **kwargs ):
        logger.debug( "POST DATA: %s" % json.dumps(request.POST, indent=4, separators=(',', ': ')) )
        logger.debug( "SESSION DATA: %s" % json.dumps(request.session.keys(), indent=4, separators=(',', ': ')) )


        # Get Therapist from session
        if 'therapist_id' in request.session.keys():
            therapist = Therapist.objects.get( id = request.session['therapist_id'] )
        else:
            return HttpResponseRedirect( reverse( 'therapist:LoginView' ) )
 
        # Get Client if in post
        client = None
        if 'client_id' in request.POST.keys():
            client = Client( client_id=request.POST['client_id'] )
        if not client:
            raise Http404

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.client = client
        form.therapist = therapist

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)