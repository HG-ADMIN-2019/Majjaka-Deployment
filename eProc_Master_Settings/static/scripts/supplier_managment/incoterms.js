var incoterms_data = new Array();
var validate_add_attributes = [];
var incoterm = {};

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><input class="input form-control check_special_char" minlength="3" maxlength="3" name="incoterm_key" type="text" pattern="[A-Z]" style="text-transform:uppercase;" ></td>'+
    '<td><input  class="form-control check_special_char"  maxlength="50" name="description" type="text"></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
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
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "incoterm_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    //document.getElementById('id_file_data_upload').value = "";
}

//**********************************************************
function onclick_copy_update_button(data) {
        $("#error_msg_id").css("display", "none")
        $("#id_popup_tbody").empty();
        $('#display_basic_table').DataTable().destroy();
        //Reference the Table.
        var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var dropdown_values = [];
    //Loop through the CheckBoxes.
   for (var i = 1; i < checkBoxes.length; i++) {
       if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
           if(GLOBAL_ACTION == "UPDATE"){
               unique_input = '<input class="form-control" value = "'+ row.cells[1].innerHTML +'" name="incoterm_key" maxlength="3"  type="text" readonly>'
                 edit_basic_data += '<tr><td hidden><input type="checkbox"></td>'+
                 '<td>'+ unique_input +'</td>'+
                  '<td><input class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" name="description" maxlength="50" type="text" ></td>'+
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
          }
          else{
                unique_input = '<input class="form-control check_special_char" value = "'+ row.cells[1].innerHTML +'" name="incoterm_key" maxlength="3" type="text" pattern="[A-Z]" style="text-transform:uppercase;">'
                 edit_basic_data += '<tr><td><input type="checkbox" required></td>'+
                 '<td>'+ unique_input +'</td>'+
                  '<td><input class="form-control check_special_char" value="' + row.cells[2].innerHTML + '" maxlength="50" name="description" type="text" ></td>'+
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
          }
       }
   }
    $('#id_popup_tbody').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);

    $('#myModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_incoterm_key").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
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

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><input class="form-control check_special_char" name="incoterm_key" minlength="3" maxlength="3" type="text" pattern="[A-Z]" style="text-transform:uppercase;"></td>'+
    '<td><input class="form-control check_special_char" name="description" maxlength="50" type="text"></td>'+
    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "incoterm_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_incoterm_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_incoterm_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.incoterm_key + '</td><td>' + item.description + '</td></tr>';
    });
    $('#id_incoterm_tbody').append(edit_basic_data);
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
// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     incoterms_data = new Array();
     validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            incoterm = {};
            incoterm.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
            incoterm.description = row.find("TD").eq(2).find('input[type="text"]').val();
            incoterm.incoterm_key = row.find("TD").eq(1).find('input[type="text"]').val();
            if (incoterm == undefined) {
                incoterm.incoterm_key = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            validate_add_attributes.push(incoterm.incoterm_key);
            incoterms_data.push(incoterm);
        });
    $('#id_save_confirm_popup').modal('show');
});
