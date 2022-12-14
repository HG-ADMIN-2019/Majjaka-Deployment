var orgnodetyp_data = new Array();
var validate_add_attributes = [];
var org_node_type = {};


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



function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    $('#display_basic_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var unique_input = '';
    var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){

                guid = row.cells[3].innerHTML
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td>'+
                '<td><select type="text" class="input form-control" id="nodetype" name="nodetype" disabled>'+ node_type_dropdown +'</select></td>'+
                '<td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="30" style="text-transform:uppercase" required></td>'+'<td hidden><input value="' + guid + '"></td>'
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                 $("#header_select").prop("hidden", true);
            }
            else if (GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                edit_basic_data += '<tr><td><input type="checkbox" required></td>'+
                '<td><select type="text" class="input form-control" id="nodetype" name="nodetype">'+ node_type_dropdown +'</select></td>'+
                '<td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="30" style="text-transform:uppercase" required></td>'+'<td hidden><input value="' + guid + '"></td>'
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';  
                $("#header_select").prop("hidden", false);
            }
            else if (GLOBAL_ACTION == "DELETE"){
                if ((row.cells[4].innerHTML=="False") || (row.cells[4].innerHTML=="false")){
                    check = '<input type="checkbox" disabled>'
                    document.getElementById('delete_data').style.visibility='hidden';
                }
                else
                {
                    check = '<input type="checkbox">'
                    document.getElementById('delete_data').style.visibility = 'visible'
                  
                }
            var node_type = row.cells[1].innerHTML;
            var node_type_desc = row.cells[2].innerHTML;
            dropdown_values.push([node_type, node_type_desc])
            guid = row.cells[3].innerHTML;
            unique_input = '<input type="text" class="input form-control"  value="' + row.cells[1].innerHTML + '" id="nodetype" name="nodetype">'
            edit_basic_data += '<tr><td>'+check+'</td><td>'+unique_input+'</td><td><input type="text" class="input form-control"  value="' + row.cells[2].innerHTML + '"  id="nodetype" name="nodetype"></td><td hidden><input value"'+guid+'"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td class="id_del_ind_checkbox1" hidden><input type="checkbox" name = "del_ind_flag" required></td></tr>';
            $("#header_select").prop("hidden", false);
           
            }
        }
    }

    
      
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
    $("#id_error_msg_org_node_type_code").prop("hidden", true);
    $("#id_error_msg_org_node_type_name").prop("hidden", true);
    $("#id_error_msg_org_node_type_length").prop("hidden", true);
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



function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var org_node_type_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        node_type = row.find("TD").eq(1).find("select option:selected").val();


        if (org_node_type_code_check.includes(node_type)) {
            $(row).remove();
        }

        org_node_type_code_check.push(node_type);


    });
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];
   // var orgnodetyp_data = new Array();
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        org_node_type = {};
        org_node_type.del_ind_flag = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        org_node_type.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        org_node_type.node_type = row.find("TD").eq(1).find("select").val();
        org_node_type.description = row.find("TD").eq(2).find("input").val();
        org_node_type.node_type_guid = row.find("TD").eq(3).find('input').val();
        if (org_node_type == undefined) {
            org_node_type.node_type = row.find("TD").eq(1).find("select").val();
        }
        
        if(org_node_type.node_type_guid == undefined) {
            org_node_type.node_type_guid = '';
        }
        validate_add_attributes.push(org_node_type.node_type);
        orgnodetyp_data.push(org_node_type);
    });

    $('#id_save_confirm_popup').modal('show');
});

