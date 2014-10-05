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


def format_submission( sdict ):

    '''
    "forage_height": "98", 
    "water_table_depth": "14", 
    "soil_type": "sand", 
    "application_equipment": "below_application", 
    "soil_moisture": "80", 
    "dairy_farm_name": "asdfdfd", 
    "manure_setback_distance": "", 
    "surface_condition": "ponding", 
    "apply_date": "9/4/2014", 
    "forage_density": "80", 
    "critical_area": "no", 
    "precipitation_2": "0.4", 
    "precipitation_1": "0.3", 
    "csrfmiddlewaretoken": "OF4PV3ypg0SUxHkhEgnp0621rUE3JltJ", 
    "managment_unit": "asdfd67"
    '''
    record = {}
    record[ 'headers' ] = [ 
        'Farm_Name' ,
        'Apply_Date' ,
        'Field_Unit' ,
        '24_Precip' ,
        '72_Precip' ,
        'Soil_Type' ,
        'Soil_Mois' ,
        'WaterT_Depth' ,
        'Forage_Density' ,
        'Forage_Height' ,
        'Surface_Condition' ,
        'App_Equipment' ,
        'Critical_Area' ,
        'Manure_Setback' ,
        'Vegitative_Buffer' ,
    ]

    record[ 'row' ] = [
        sdict.get( 'dairy_farm_name', '' ) ,
        sdict.get( 'apply_date', '' ) , 
        sdict.get( 'management_unit', '' ) ,
        sdict.get( 'precipitation_1', '' ) ,
        sdict.get( 'precipitation_2', '' ) ,
        sdict.get( 'soil_type', '' ) ,
        sdict.get( 'soil_moisture', '' ) ,
        sdict.get( 'water_table_depth', '' ) ,
        sdict.get( 'forage_density', '' ) ,
        sdict.get( 'forage_height', '' ) ,
        sdict.get( 'surface_condition', '' ) ,
        sdict.get( 'application_equipment', '' ) ,
        sdict.get( 'critical_area', '' ) ,
        sdict.get( 'manure_setback_distance', '' ) ,
        sdict.get( 'vegetation_buffer', '' ) ,
    ]

    return record



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
            format = format_submission( self.request.POST )
            fsock.write( ','.join( format[ 'headers' ] ) + "\n" )
            fsock.write( ','.join( format[ 'row' ] ) + "\n" )

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
        return super( WorksheetView, self ).form_valid( form )

    def post( self, request, *args, **kwargs ):

        logger.debug( "[ POST PARAMS ]: %s" % json.dumps( request.POST, indent=4 ) )

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.set_success_url()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


