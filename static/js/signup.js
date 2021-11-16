$(document).ready(function () {
    // Countries
    var country_arr = new Array("Select Country", "AUSTRALIA", "INDIA", "NEW ZEALAND", "USA", "UAE", "MAURITIUS");

    $.each(country_arr, function (i, item) {
        $('#id_address-país').append($('<option>', {
            value: i,
            text: item,
        }, '</option>'));
    });

    // States
    var s_a = new Array();
    s_a[0] = "Select State";
    s_a[1] = "Select State|QUEENSLAND|VICTORIA";
    s_a[2] = "Select State|ANDHRAPRADESH|KARNATAKA|TAMILNADU|DELHI|GOA|W-BENGAL|GUJARAT|MADHYAPRADESH|MAHARASHTRA|RAJASTHAN";
    s_a[3] = "Select State|AUCKLAND";
    s_a[4] = "Select State|NEWJERSEY|ILLINOIS";
    s_a[5] = "Select State|DUBAI";
    s_a[6] = "Select State|MAURITIUS";

    // Cities
    var c_a = new Array();
    c_a['QUEENSLAND'] = "BRISBANE";
    c_a['VICTORIA'] = "MELBOURNE";
    c_a['ANDHRAPRADESH'] = "HYDERABAD";
    c_a['KARNATAKA'] = "BANGLORE";
    c_a['TAMILNADU'] = "CHENNAI";
    c_a['DELHI'] = "DELHI";
    c_a['GOA'] = "GOA";
    c_a['W-BENGAL'] = "KOLKATA";
    c_a['GUJARAT'] = "AHMEDABAD1|AHMEDABAD2|AHMEDABAD3|BARODA|BHAVNAGAR|MEHSANA|RAJKOT|SURAT|UNA";
    c_a['MADHYAPRADESH'] = "INDORE";
    c_a['MAHARASHTRA'] = "MUMBAI|PUNE";
    c_a['RAJASTHAN'] = "ABU";
    c_a['AUCKLAND'] = "AUCKLAND";
    c_a['NEWJERSEY'] = "EDISON";
    c_a['ILLINOIS'] = "CHICAGO";
    c_a['MAURITIUS'] = "MAURITIUS";
    c_a['DUBAI'] = "DUBAI";


    $('#id_address-país').change(function () {
        var c = $(this).val();
        var state_arr = s_a[c].split("|");
        $('#id_address-estado').empty();
        $('#id_address-ciudad').empty();
        if (c == 0) {
            $('#state').append($('<option>', {
                value: '0',
                text: 'Select State',
            }, '</option>'));
        } else {
            $.each(state_arr, function (i, item_state) {
                $('#id_address-estado').append($('<option>', {
                    value: item_state,
                    text: item_state,
                }, '</option>'));
            });
        }
        $('#id_address-ciudad').append($('<option>', {
            value: '0',
            text: 'Select City',
        }, '</option>'));
    });

    $('#id_address-estado').change(function () {
        var s = $(this).val();
        if (s == 'Select State') {
            $('#id_address-ciudad').empty();
            $('#id_address-ciudad').append($('<option>', {
                value: '0',
                text: 'Select City',
            }, '</option>'));
        }
        var city_arr = c_a[s].split("|");
        $('#id_address-ciudad').empty();

        $.each(city_arr, function (j, item_city) {
            $('#id_address-ciudad').append($('<option>', {
                value: item_city,
                text: item_city,
            }, '</option>'));
        });
    });
});