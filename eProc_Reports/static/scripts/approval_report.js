    // Script to generate sort and filter feature for tables
    $(document).ready(function () {
        nav_bar_admin();
        table_sort_filter_export_excel();

        // Loader implementation on search button
        $('#hg_approval_report_search').click(function () {
            $('#hg_loader').modal('show');
        });
        // Bootstrap-select plugin being called to render multiselect dropdown
    $('.multiple_select').selectpicker();
    $('.multiple_select').selectpicker('val', selected_status_value);


//     var x = document.getElementById("acc_assgn_cat");
//     x.add(option, option.defaultSelected, x[0] );
//    x.add(option, 0 ); //add as the first item, always
//    x.selectedIndex = 0;

    $('#id_comp_code_app').val(selected_comp_value).attr('selected', 'selected');
    $('#acc_assgn_cat').val(selected_status_value).attr('selected', 'selected');

    });

    // Function to store the data into the session
    window.onbeforeunload = function () {
        sessionStorage.setItem("COMP_CODE", $('#id_comp_code_app').val());
        sessionStorage.setItem("ACC_ASSGN_CAT", $('#acc_assgn_cat').val());
//           $('.multiple_select').selectpicker('val', selected_status_value);
//           $('select option:first-child').attr("selected", "selected");
    }

    // Function to retrieve data from session storage
    window.onload = function () {
        comp_code = sessionStorage.getItem("COMP_CODE");
        acc_assgn_cat = sessionStorage.getItem("ACC_ASSGN_CAT");

        $('#id_comp_code_app').val(comp_code).attr('selected', 'selected');
        $('#acc_assgn_cat').val(acc_assgn_cat).attr('selected', 'selected');
//        $('.multiple_select').selectpicker('val', selected_status_value);
//        $('select option:first-child').attr("selected", "selected");
    }

    $('#hg_approval_report_search').click(function () {
        OpenLoaderPopup();
    })