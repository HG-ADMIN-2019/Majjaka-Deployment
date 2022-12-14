var prodcat_data = new Array();
var validate_add_attributes = [];
var prodcat={};

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><input class="input form-control check_number" type="text" title="Minimum length is 2" minlength="10" maxlength="10"  name="prod_cat_id" required></td>'+
    '<td><input class="input form-control check_special_char" type="text" maxlength="20" name="prod_cat_desc" required></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
    '<td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>'
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
    $('#delete_data').hide()
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "prodcat_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";

}

// on click copy icon display the selected checkbox data
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

function onclick_copy_update_button(data) {
    $("#error_msg_id").css("display", "none")
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();

       //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var unique_input = '';
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                unique_input = '<input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="prod_cat_id"  maxlength="20"  disabled>'
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td><td>'+unique_input+'</td><td><input type="text" class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" name="prod_cat_desc"  maxlength="100" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            else if (GLOBAL_ACTION == "COPY"){
                unique_input = '<input class="form-control check_number" type="text" value="' + row.cells[1].innerHTML + '" name="prod_cat_id"  maxlength="20"  required>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td><td>'+unique_input+'</td><td><input type="text" class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" name="prod_cat_desc"  maxlength="100" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>';
                $("#header_select").prop("hidden", false);
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

        }
    }

    display_button()
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#myModal').modal('show');
    table_sort_filter('id_popup_table');
    table_sort_filter('display_basic_table');
    
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
    $("#id_error_msg_prodcat").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();


});



function display_error_message(error_message){

        $('#error_message').text(error_message);
        //$("p").css("color", "red");
        //document.getElementById("error_message").innerHTML = error_message;
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}


// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("No records to be saved");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><input class="input form-control check_number" type="text" title="Minimum length is 2" minlength="3" maxlength="10"  name="prod_cat_id" required></td>'+
     '<td><input class="input form-control check_special_char" type="text" maxlength="20"  name="prod_cat_desc"  required></td>'+
     '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
     '<td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "prodcat_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    $('#delete_data').hide()
    table_sort_filter_popup('id_popup_table');
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_prodcat_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_prodcat_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.prod_cat_id + '</td><td>' + item.prod_cat_desc + '</td><td hidden>' + item.del_ind_flag  + '</td></tr>';
    });
    $('#id_prodcat_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
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


//deletes he duplicate data
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var prod_cat_id_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        prod_cat_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')


        if (prod_cat_id_check.includes(prod_cat_id)) {
            $(row).remove();
        }

        prod_cat_id_check.push(prod_cat_id);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    prodcat_data = new Array();
    validate_add_attributes = [];
   $("#id_popup_table TBODY TR").each(function () {
           var row = $(this);
           prodcat={};
           prodcat.del_ind_flag = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
           prodcat.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
           prodcat.prod_cat_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
           prodcat.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
           if (prodcat == undefined){
            prodcat. prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val();
            }

           validate_add_attributes.push(prodcat.prod_cat_id);
           prodcat_data.push(prodcat);
       });
    $('#id_save_confirm_popup').modal('show');
});




