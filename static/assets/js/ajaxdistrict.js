
    $("#id_province").change(function(){
        const url = $("#form_province").attr("data-district-url");  // get the url of the `load_cities` view
        console.log(url)
        const provinceid = $(this).val(); 
        
       
        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
            data: {
                'provinceid': provinceid       // add the country id to the GET parameters
            },
            success: function(data) {   // `data` is the return of the `load_cities` view function
                $("#id_district").html(data); 

              
            }
        });

    });
