    /*
    **
    **  FUNCTIONS
    **
    */
    function has_input_date_support() {
        var input = document.createElement('input');
        input.setAttribute('type','date');

        var notADateValue = 'not-a-date';
        input.setAttribute('value', notADateValue); 

        return !(input.value === notADateValue);
    } 


    /*
    **
    **  ON READY
    **
    */
    $(document).ready(function() {

        /*
        // if browser doesn't support date input, create text input
        if ( !has_input_date_support() ) {
            $( 'input#apply_date' ).prop( 'type', 'text' );    
        }
        */


        var form_selector = '#arm_form';
        window.validator_ref = null;
        $( form_selector )
            .on('init.field.bv', function(e, data) {

                // $(e.target)  --> The field element
                // data.bv      --> The BootstrapValidator instance
                // data.field   --> The field name
                // data.element --> The field element
                
                if ( window.validator_ref === null ) {
                    validator_ref = data.bv;
                }

            })
            .bootstrapValidator({

                fields : {
                    soil_moisture : {
                        validators : {
                            restrict : {
                                value : 90 ,
                                message : 'fuck yeah'
                            }
                        } ,
                    } ,
                } ,

            })
            .on( 'success.field.bv', function( e, data ) {
                console.log( "[ VALIDATE ]: " + data.validator + ' for ' + data.field, data );

                // $(e.target)  --> The field element
                // data.bv      --> The BootstrapValidator instance
                // data.field   --> The field name
                // data.element --> The field element


                // skip fields that do not have any stop validation
                if ( data.field in window.CONFIG.fields_without_stop_validation ) {
                    return;
                }


                // SOIL MOISTURE
                if ( data.field === 'soil_moisture' ) {
                    var selected_value = $( e.target ).parents( ".form-group" ).find( "input:checked" ).val();
                    var restricted_value = $( e.target ).attr( 'data-arm-restricted-value' );
                    if ( parseInt( selected_value ) >= parseInt( restricted_value ) ) {
                    }
                }


                

                
            });

    }); //  ready

