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
from django.core.mail import send_mail, BadHeaderError, EmailMessage


#
#  sys imports
#
import json
import uuid
import io
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
        self.success_url = reverse( 'thankyou', )

    def form_valid( self, form ):
        '''
        email = EmailMessage('ARM worksheet submission', 'please see attachement', 'no_reply@whatcomcd-arm.com',
                    ['gregcorradini@gmail.com'], ['bcc@example.com'],
                    headers = {'Reply-To': 'another@example.com'})
        '''
        filename = 'submission-'+str(uuid.uuid4())+'.csv'
        logger.debug( "[ WRITING FILE ]: %s" % filename )
        with open( '/tmp/'+filename, 'w' ) as fsock:
            fsock.write( json.dumps( self.request.POST, indent=4 ) )

        try:
            email = EmailMessage(
                        'ARM worksheet submission', 
                        'please see attachement', 
                        'no_reply@whatcomcd-arm.com',
                        ['gregcorradini@gmail.com'], [],
                        headers = {})
            email.attach_file('/tmp/'+filename)
            email.send()
        except Exception as e:
            logger.exception( e );
        super( WorksheetView, self ).form_valid( form )

    def post( self, request, *args, **kwargs ):

        logger.debug( "[ POST PARAMS ]: %s" % json.dumps( request.POST, indent=4 ) )

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.set_success_url()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


