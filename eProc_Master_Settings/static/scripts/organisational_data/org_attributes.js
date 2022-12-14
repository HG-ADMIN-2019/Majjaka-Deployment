var orgattr_data = new Array();
var validate_add_attributes = [];
var org_attr={};


/// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";    
}

function onclick_delete_button() {
    GLOBAL_ACTION = "DELETE"
    onclick_copy_update_button("DELETE")
    document.getElementById("id_del_add_button").style.display = "none";
}

function onclick_copy_update_button() {
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = document.getElementsByClassName("checkbox_check");
    var edit_basic_data = "";
    var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){

                edit_basic_data +=  '<tr><td hidden><input type="checkbox" required></td><td><select type="text" class="input form-control" id="attributeid"  name="attributeid" disabled>'+ attribute_id_dropdown_onload +'</select></td></td><td><input class="form-control attribute_name" type="text" value="' + row.cells[2].innerHTML + '" name="attribute_name" id="attribute_name-1" disabled></td><td><input type="checkbox"  name="range_indicator" required></td><td><input type="checkbox"  name="multiple_value" required></td><td><input type="checkbox" name="allow_defaults" required></td><td><input type="checkbox"  name="inherit_values" required></td><td><input type="number" value="' + row.cells[7].innerHTML + '" name="maxlength"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
	             $("#header_select").prop("hidden", true);

            }
            else if (GLOBAL_ACTION == "COPY"){

               edit_basic_data +=  '<tr><td><input type="checkbox" required></td><td><select type="text" class="input form-control attribute" id="attribute-1"  name="attribute" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ attribute_id_dropdown +'</select></td>td><input class="form-control attribute_name" type="text" value="' + row.cells[2].innerHTML + '" name="attribute_name" id="attribute_name-1" disabled></td><td><input type="checkbox"  name="range_indicator" required></td><td><input type="checkbox"  name="multiple_value" required></td><td><input type="checkbox"  name="allow_defaults" required></td><td><input type="checkbox" name="inherit_values" required></td><td><input type="number" value="' + row.cells[7].innerHTML + '" name="maxlength"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
	           $("#header_select").prop("hidden", false);<
            }
            else if (GLOBAL_ACTION == "DELETE"){
                if ((row.cells[3].innerHTML=="False") || (row.cells[3].innerHTML=="false")){
                    check = '<input type="checkbox" disabled>'
                    document.getElementById('delete_data').style.visibility='hidden';
                }
                else
                {
                    check = '<input type="checkbox">'
                    document.getElementById('delete_data').style.visibility = 'visible'
                  
                }
                unique_input = '<input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="prod_cat_id" onkeypress="return /[0-9]/i.test(event.key)" maxlength="20" style="text-transform:uppercase" required>'
                edit_basic_data += '<tr><td>'+check+'</td><td>'+unique_input+'</td><td><input type="text" class="form-control" value="' + row.cells[2].innerHTML + '" name="prod_cat_desc" onkeypress="return /[a-z ]/i.test(event.key)" maxlength="100" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>';
                $("#header_select").prop("hidden", false);


            }

            var attribute = row.cells[1].innerHTML
            var range_indicator = row.cells[3].children.range_indicator.checked
            var multiple_value = row.cells[4].children.multiple_value.checked
            var allow_defaults = row.cells[5].children.allow_defaults.checked
            var inherit_values = row.cells[6].children.inherit_values.checked
            dropdown_values.push([ attribute,range_indicator,multiple_value,allow_defaults,inherit_values])
      }
    }
   
    var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var attribute = dropdown_values[i][0]
        var range_indicator = dropdown_values[i][1];
        var multiple_value = dropdown_values[i][2];
        var allow_defaults = dropdown_values[i][3];
        var inherit_values = dropdown_values[i][4];

        $(row.find("TD").eq(1).find("select option[value=" + attribute + "]")).attr('selected', 'selected');
        if(range_indicator) {
            $(row.find("TD").eq(3).find('input[name="range_indicator"]').attr('checked', 'checked'));
        }
        if(multiple_value) {
            $(row.find("TD").eq(4).find('input[name="multiple_value"]').attr('checked', 'checked'));
        }
        if(allow_defaults) {
            $(row.find("TD").eq(5).find('input[name="allow_defaults"]').attr('checked', 'checked'));
        }
        if(inherit_values) {
            $(row.find("TD").eq(6).find('input[name="inherit_values"]').attr('checked', 'checked'));
        }
        
        i++;
      });
        display_button()
        $('#id_popup_tbody').append(edit_basic_data);
        $("#id_del_ind_checkbox").prop("hidden", true);
        $('#myModal').modal('show');
        table_sort_filter('display_basic_table');
        table_sort_filter('id_popup_table');
}

function display_button(){
    if(GLOBAL_ACTION == "DELETE"){
        $('#delete_data').show();
        $('#save_id').hide();
       
    }
    else{
        $('#delete_data').hide();
        $('#save_id').show();

    }


}



//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_org_attr_code").prop("hidden", true);
    $("#id_error_msg_org_attr_name").prop("hidden", true);
    $("#id_error_msg_org_attr_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


function display_error_message(error_message){

    $('#error_message').text(error_message);

    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');

}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_org_attr_tbody').empty();
    var edit_basic_data = '';

    $.each(rendered_org_attr_data, function (i, item) {
            var data = '';
            var data1 = '';
            var data2 = '';
            var data3 = '';
            if (item.range_indicator == true){
                data = '<input type="checkbox" name="range_indicator" value="" checked disabled>'
            } else{
                data = '<input type="checkbox" name="range_indicator" value="" disabled>'
            }
             if (item.multiple_value == true){
                data1 = '<input type="checkbox" name="multiple_value" value="" checked disabled>'
            } else{
                data1 = '<input type="checkbox" name="multiple_value" value="" disabled>'
            }
             if (item.allow_defaults == true){
                data2 = '<input type="checkbox" name="allow_defaults" value="" checked disabled>'
            } else{
                data2 = '<input type="checkbox" name="allow_defaults" value="" disabled>'
            }
            if (item.inherit_values == true){
                data3 = '<input type="checkbox" name="inherit_values" value="" checked disabled>'
            } else{
                data3 = '<input type="checkbox" name="inherit_values" value="" disabled>'
            }
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.attribute_id + '</td><td>' + item.attribute_name + '</td>'+
        '<td>' + data + '</td>' +
        '<td>' + data1 + '</td>' +
        '<td>' + data2 + '</td>' +
        '<td>' + data3 + '</td>' +
        '<td>' + item.maximum_length + '</td>' +
        '<td hidden> '+ item.del_ind_flag+'</td></tr>';
    });
    $('#id_org_attr_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input.checkbox_check:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    $('#id_check_all').hide();
    table_sort_filter('display_basic_table');
}



function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var org_attr_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        attribute_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();

        if (org_attr_code_check.includes(attribute_id)) {
            $(row).remove();
        }
        org_attr_code_check.push(attribute_id);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        org_attr = {};
        org_attr.del_ind_flag = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        org_attr.del_ind = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        org_attr.attribute_id = row.find("TD").eq(1).find('select[type="text"]').val();
        org_attr.attribute_name = row.find("TD").eq(2).find('input[type="text"]').val();
        org_attr.range_indicator =row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        org_attr.multiple_value = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        org_attr.allow_defaults = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        org_attr.inherit_values =row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        org_attr.maximum_length = row.find("TD").eq(7).find('input[type="number"]').val()
        if (org_attr == undefined) {
            org_attr.attribute_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }


        validate_add_attributes.push(org_attr.attribute_id);
        orgattr_data.push(org_attr);
    });


    $('#id_save_confirm_popup').modal('show');
});



