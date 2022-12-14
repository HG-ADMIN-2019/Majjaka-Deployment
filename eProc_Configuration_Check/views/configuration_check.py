from django.http import JsonResponse

from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Configuration_Check.Utilities.configuration_check_generic import check_unspsc_category_desc_data, \
    check_unspsc_category_data, check_acc_assign_desc_data, check_acc_assign_values_data, check_company_data, \
    check_purchaseorg_data, check_purchasegrp_data, check_workflowschema_data, check_approvaltype_data, \
    check_spending_limit_data, check_spendlimit_value_data, check_approv_limit_value_data, check_approv_limit_data, \
    check_address_types_data, check_workflow_acc_data, check_inco_terms_data, check_paymentterm_desc_data, \
    check_address_data
from eProc_Shopping_Cart.context_processors import update_user_info

JsonParser_obj = JsonParser()


def check_cust_unspsc_category_desc(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_unspsc_category_desc_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_cust_unspsc_category(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_unspsc_category_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_acc_assign_desc(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_acc_assign_desc_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_acc_assign_values(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_acc_assign_values_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_company(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_company_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_purchaseorg(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_purchaseorg_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_purchasegrp(request):
    """

    """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_purchasegrp_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_approvaltype(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_approvaltype_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_workflowschema(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_workflowschema_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_spendlimit_value(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_spendlimit_value_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_spending_limit(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages,valid_data = check_spending_limit_data(ui_data)
    return JsonResponse({'messages': messages,'valid_data':valid_data}, safe=False)


def check_approvlimit_value(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_approv_limit_value_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_approv_limit(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_approv_limit_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_workflow_acc(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_workflow_acc_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_address_types(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_address_types_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)



def check_address(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_address_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_inco_terms(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_inco_terms_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)


def check_paymentterm_desc(request):
    """

       """
    update_user_info(request)
    ui_data_dictionary = JsonParser_obj.get_json_from_req(request)
    ui_data = ui_data_dictionary['data_list']
    messages = check_paymentterm_desc_data(ui_data)
    return JsonResponse({'messages': messages}, safe=False)
