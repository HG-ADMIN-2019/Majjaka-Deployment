import csv
import io
from itertools import chain

from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import *

from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Basic.Utilities.functions.update_del_ind import update_del_ind, query_update_del_ind
from eProc_Basic.Utilities.messages import messages
from eProc_Basic.Utilities.messages.messages import MSG048
from eProc_Basic_Settings.Utilities.basic_settings_specific import save_basic_data_into_db, csv_data_arrangement, \
    save_language_data_into_db, save_unitofmeasures_data_into_db, save_country_data_into_db, save_currency_data_into_db, \
    save_timezone_data_into_db, save_prodcat_data_into_db, csv_preview_data
from eProc_Catalog.Utilities.catalog_generic import CatalogGenericMethods
from eProc_Catalog.Utilities.catalog_specific import CatalogManagement
from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data
from eProc_Configuration.models import *
from eProc_Configuration_Check.Utilities.configuration_check_generic import *
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData
from eProc_Shopping_Cart.context_processors import update_user_info
from eProc_Upload.Utilities.upload_data.upload_pk_tables import UploadBasicTables, CompareTableHeader

JsonParser_obj = JsonParser()
django_query_instance = DjangoQueries()


def upload_data_display(request):
    """

    :param request:
    :return:
    """
    # Basic Settings Table logic

    upload_data = request.POST.get('upload_table_name')

    client = getClients(request)

    if upload_data == 'upload_country':
        upload_data_response = ''
        upload_data_response = Country.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)
    elif upload_data == 'upload_currencies':
        upload_data_response = ''
        upload_data_response = Currency.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)
    elif upload_data == 'upload_languages':
        upload_data_response = Languages.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)
    elif upload_data == 'upload_ProdCat':
        upload_data_response = UnspscCategories.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)
    elif upload_data == 'upload_Timezone':
        upload_data_response = TimeZone.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)
    elif upload_data == 'upload_UOM':
        upload_data_response = UnitOfMeasures.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)

    # Application settings tables

    elif upload_data == 'upload_clients':
        upload_data_response = OrgClients.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)
    elif upload_data == 'upload_doctyp':
        upload_data_response = DocumentType.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)
    elif upload_data == 'upload_accasscat':
        upload_data_response = AccountAssignmentCategory.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)

    # Master Data Settings tables
    elif upload_data == 'upload_apptypes':
        upload_data_apptypes = ApproverType.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_apptypes)


    elif upload_data == 'upload_accdata':
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_acccat = AccountAssignmentCategory.objects.filter(del_ind=False)
        upload_data_response = AccountingData.objects.filter(client=client, del_ind=False)
        Accdata_attributes = list(chain(upload_data_response, upload_data_acccat, upload_data_company))
        return JsonParser_obj.get_json_from_obj(Accdata_attributes)

    elif upload_data == 'upload_accdatades':
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_acccat = AccountAssignmentCategory.objects.filter(del_ind=False)
        upload_data_acc_desc = AccountingDataDesc.objects.filter(client=client, del_ind=False)
        upload_data_language = Languages.objects.filter(del_ind=False)
        Accdatades_attributes = list(
            chain(upload_data_acc_desc, upload_data_acccat, upload_data_language, upload_data_company))
        return JsonParser_obj.get_json_from_obj(Accdatades_attributes)

    elif upload_data == 'upload_applimit':
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_app_lim = ApproverLimit.objects.filter(client=client, del_ind=False)
        Applimit_attributes = list(chain(upload_data_app_lim, upload_data_company))
        return JsonParser_obj.get_json_from_obj(Applimit_attributes)

    elif upload_data == 'upload_applimval':
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_currency = Currency.objects.filter(del_ind=False)
        upload_data_apptypes = ApproverType.objects.filter(del_ind=False)
        upload_data_app_lim_val = ApproverLimitValue.objects.filter(client=client, del_ind=False)
        Applimitval_attributes = list(
            chain(upload_data_app_lim_val, upload_data_apptypes, upload_data_company, upload_data_currency))
        return JsonParser_obj.get_json_from_obj(Applimitval_attributes)


    elif upload_data == 'upload_spndlimid':
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_spnd_lim_id = SpendLimitId.objects.filter(client=client, del_ind=False)
        Spndlimit_attributes = list(chain(upload_data_spnd_lim_id, upload_data_company))
        return JsonParser_obj.get_json_from_obj(Spndlimit_attributes)

    elif upload_data == 'upload_spndlimval':
        upload_data_currency = Currency.objects.filter(del_ind=False)
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_spnd_lim_val = SpendLimitValue.objects.filter(client=client, del_ind=False)
        SpndlimitValue_attributes = list(chain(upload_data_spnd_lim_val, upload_data_company, upload_data_currency))
        return JsonParser_obj.get_json_from_obj(SpndlimitValue_attributes)

    elif upload_data == 'upload_wfschema':
        upload_data_apptypes = ApproverType.objects.filter(del_ind=False)
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_wfschema = WorkflowSchema.objects.filter(client=client, del_ind=False)
        WfSchema_attributes = list(chain(upload_data_wfschema, upload_data_company, upload_data_apptypes))
        return JsonParser_obj.get_json_from_obj(WfSchema_attributes)

    elif upload_data == 'upload_WFACC':
        upload_data_acccat = AccountAssignmentCategory.objects.filter(del_ind=False)
        upload_data_wfacc = WorkflowACC.objects.filter(client=client, del_ind=False)
        upload_data_currency = Currency.objects.filter(del_ind=False)
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        WFACC_attributes = list(chain(upload_data_wfacc, upload_data_acccat, upload_data_currency, upload_data_company))
        return JsonParser_obj.get_json_from_obj(WFACC_attributes)

    elif upload_data == 'upload_orgnodetypes':
        upload_data_orgnodetypes = OrgNodeTypes.objects.filter(client=client, del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_orgnodetypes)

    elif upload_data == 'upload_orgattributes':
        upload_data_OrgAttributes = OrgAttributes.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_OrgAttributes)

    elif upload_data == 'upload_companies':
        upload_data_Orgmodel = OrgModel.objects.filter(client=client, del_ind=False)
        upload_data_OrgCompanies = OrgCompanies.objects.filter(client=client, del_ind=False)
        OrgCompanies_attributes = list(chain(upload_data_OrgCompanies, upload_data_Orgmodel))
        return JsonParser_obj.get_json_from_obj(OrgCompanies_attributes)

    elif upload_data == 'upload_porg':
        upload_data_Orgmodel = OrgModel.objects.filter(client=client, del_ind=False)
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_OrgPorg = OrgPorg.objects.filter(client=client, del_ind=False)
        OrgPorg_attributes = list(chain(upload_data_OrgPorg, upload_data_Orgmodel, upload_data_company))
        return JsonParser_obj.get_json_from_obj(OrgPorg_attributes)

    elif upload_data == 'upload_pgrp':
        upload_data_Orgmodel = OrgModel.objects.filter(client=client, del_ind=False)
        upload_data_company = OrgCompanies.objects.filter(client=client, del_ind=False)
        upload_data_OrgPorg = OrgPorg.objects.filter(client=client, del_ind=False)
        upload_data_OrgPGroup = OrgPGroup.objects.filter(client=client, del_ind=False)
        OrgPgroup_attributes = list(
            chain(upload_data_OrgPGroup, upload_data_Orgmodel, upload_data_OrgPorg, upload_data_company))
        return JsonParser_obj.get_json_from_obj(OrgPgroup_attributes)

    elif upload_data == 'upload_roles':
        upload_data_response = ''
        upload_data_response = UserRoles.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)

    elif upload_data == 'upload_authobj':
        upload_data_response = ''
        upload_data_response = AuthorizationObject.objects.filter(del_ind=False)
        return JsonParser_obj.get_json_from_obj(upload_data_response)

    elif upload_data == 'upload_authgrp':
        upload_data_response = ''
        upload_data_AuthorizationGroup = AuthorizationGroup.objects.filter(del_ind=False)
        upload_data_AuthorizationObject = AuthorizationObject.objects.filter(del_ind=False)
        upload_data_response = list(chain(upload_data_AuthorizationGroup, upload_data_AuthorizationObject))
        return JsonParser_obj.get_json_from_obj(upload_data_response)

    elif upload_data == 'upload_auth':
        upload_data_response = ''
        upload_data_Authorization = Authorization.objects.filter(client=client, del_ind=False)
        upload_data_UserRoles = UserRoles.objects.filter(del_ind=False)
        upload_data_response = list(chain(upload_data_Authorization, upload_data_UserRoles))
        return JsonParser_obj.get_json_from_obj(upload_data_response)


def create_update_basic_data(request):
    """

    """
    update_user_info(request)
    basic_data = JsonParser_obj.get_json_from_req(request)
    if basic_data['table_name'] == 'Country':
        display_data = save_country_data_into_db(basic_data)
        basic_data['data'] = get_valid_country_data(basic_data['data'])
        return JsonResponse(display_data, safe=False)
    if basic_data['table_name'] == 'Languages':
        display_data = save_language_data_into_db(basic_data)
        basic_data['data'] = get_valid_language_data(basic_data['data'])
        return JsonResponse(display_data, safe=False)
    if basic_data['table_name'] == 'UnitOfMeasures':
        display_data = save_unitofmeasures_data_into_db(basic_data)
        basic_data['data'] = get_valid_uom_data(basic_data['data'])
        return JsonResponse(display_data, safe=False)
    if basic_data['table_name'] == 'Currency':
        display_data = save_currency_data_into_db(basic_data)
        basic_data['data'] = get_valid_currency_data(basic_data['data'])
        return JsonResponse(display_data, safe=False)
    if basic_data['table_name'] == 'TimeZone':
        display_data = save_timezone_data_into_db(basic_data)
        basic_data['data'] = get_valid_timezone_data(basic_data['data'])
        return JsonResponse(display_data, safe=False)


def save_basic_data(request):
    """

    :param request:
    :return:
    """
    basic_data = JsonParser_obj.get_json_from_req(request)
    Table_name = basic_data['Dbl_clck_tbl_id']
    del basic_data['Dbl_clck_tbl_id']

    basic_data_list = []

    for value in basic_data.values():
        basic_data_list.append(value)

    upload_data_response = save_basic_data_into_db(basic_data_list, Table_name)
    return JsonResponse(upload_data_response, safe=False)


def upload_countries(request):
    upload_country = get_configuration_data(Country, {'del_ind': False}, ['country_code', 'country_name'])
    # str = 'hello'
    # print(str.upper())
    return render(request, 'Basic_setting_Upload/upload_countries.html',
                  {'upload_countries': upload_country,
                   'inc_nav': True})


def upload_languages(request):
    upload_language = get_configuration_data(Languages, {'del_ind': False}, ['language_id', 'description'])
    return render(request, 'Basic_setting_Upload/upload_languages.html',
                  {'upload_languages': upload_language,
                   'inc_nav': True})


def upload_unit_of_measure(request):
    upload_unitofmeasures = get_configuration_data(UnitOfMeasures, {'del_ind': False},
                                                   ['uom_id', 'uom_description', 'iso_code_id'])
    return render(request, 'Basic_setting_Upload/upload_unit_of_measure.html',
                  {'upload_unit_of_measure': upload_unitofmeasures,
                   'inc_nav': True})


def data_upload(request):
    db_header = request.POST.get('db_header_data')
    csv_file = request.FILES['file_attach']
    data_set_val = csv_file.read().decode('ISO-8859-1')
    # fin_upload_data = io.StringIO(data_set_val)

    upload_csv = CompareTableHeader()
    result = {}
    # upload_csv.header_data = fin_upload_data
    upload_csv.app_name = request.POST.get('appname')
    upload_csv.table_name = request.POST.get('Tablename')
    upload_csv.request = request
    fin_data_upload_header = io.StringIO(data_set_val)
    upload_csv.header_data = fin_data_upload_header
    basic_save, header_detail = upload_csv.basic_header_condition()
    # print(basic_save)
    # if not basic_save:
    try:

        result['error_message'], result['data'] = upload_csv.csv_preview_data(header_detail, data_set_val)

        # retrieving correct ordered data from csv_data_arrangement() - basic_settings_specific.py
        # correct_order_list = csv_data_arrangement(db_header, data_set_val)
        return JsonResponse(result, safe=False)

    except MultiValueDictKeyError:
        csv_file = False
        error_msg = get_message_desc(MSG048)[1]
        # msgid = 'MSG048'
        # error_msg = get_msg_desc(msgid)
        # msg = error_msg['message_desc'][0]
        # error_msg = msg
        messages.error(request, error_msg)
        # messages.error(request, MSG048)

    print(basic_save)
    # else:
    return JsonResponse(basic_save, safe=False)


class DB_count:
    pass


def upload_currencies(request):
    upload_currency = get_configuration_data(Currency, {'del_ind': False}, ['currency_id', 'description'])
    return render(request, 'Basic_setting_Upload/upload_currencies.html',
                  {'upload_currencies': upload_currency, 'inc_nav': True})


def srm_currency(request):
    upload_currency = get_configuration_data(Currency, {'del_ind': False}, ['currency_id', 'description'])
    return render(request, 'Application_Settings/srm_currency.html',
                  {'upload_currencies': upload_currency, 'inc_nav': True})


def extract_country_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_COUNTRIES_CSV

    writer = csv.writer(response)

    writer.writerow(['COUNTRY_CODE', 'COUNTRY_NAME', 'del_ind'])
    # get only active record
    countries = django_query_instance.django_filter_query(Country,
                                                          {'del_ind': False}, None,
                                                          ['country_code', 'country_name', 'del_ind'])
    country_data = query_update_del_ind(countries)

    for country in country_data:
        country_info = [country['country_code'], country['country_name'], country['del_ind']]
        writer.writerow(country_info)

    return response


def extract_country_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Countries Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(['COUNTRY_CODE', 'COUNTRY_NAME', 'del_ind'])
    return response


def extract_timezone_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Timezone Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(["TIME_ZONE", "DESCRIPTION", "UTC_DIFFERENCE", "DAYLIGHT_SAVE_RULE", "del_ind"])
    return response


def extract_currency_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Currency Template.CSV"'

    writer = csv.writer(response)

    writer.writerow(["CURRENCY_ID", "DESCRIPTION", "del_ind"])
    return response


def extract_product_category_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_PRODUCT_CATEGORY_CSV

    writer = csv.writer(response)
    writer.writerow(['PROD_CAT_ID', 'PROD_CAT_DESC', 'del_ind'])

    product_categories = django_query_instance.django_filter_query(UnspscCategories,
                                                                   {'del_ind': False}, None,
                                                                   ['prod_cat_id', 'prod_cat_desc', 'del_ind'])
    product_category_data = query_update_del_ind(product_categories)

    for product_category in product_category_data:
        product_category_info = [product_category['prod_cat_id'], product_category['prod_cat_desc'],
                                 product_category['del_ind']]
        writer.writerow(product_category_info)

    return response


def extract_client_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_CLIENT_CSV

    writer = csv.writer(response)
    writer.writerow(['CLIENT', 'DESCRIPTION', 'del_ind'])

    client_details = django_query_instance.django_filter_query(OrgClients,
                                                               {'del_ind': False}, None,
                                                               ['client', 'description', 'del_ind'])
    client_details_data = query_update_del_ind(client_details)

    for client_detail in client_details_data:
        client_detail_info = [client_detail['client'], client_detail['description'],
                              client_detail['del_ind']]
        writer.writerow(client_detail_info)


def extract_document_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_DOCUMENT_CSV

    writer = csv.writer(response)
    writer.writerow(['DOCUMENT_TYPE', 'DOCUMENT_TYPE_DESC', 'del_ind'])

    document_details = django_query_instance.django_filter_query(DocumentType,
                                                                 {'del_ind': False}, None,
                                                                 ['document_type', 'document_type_desc', 'del_ind'])
    document_details_data = query_update_del_ind(document_details)

    for document_detail in document_details_data:
        document_detail_info = [document_detail['document_type'], document_detail['document_type_desc'],
                                document_detail['del_ind']]
        writer.writerow(document_detail_info)

    return response


def extract_calendar_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_CALENDAR_CSV

    writer = csv.writer(response)
    writer.writerow(['CALENDER_ID', 'DESCRIPTION', 'COUNTRY_CODE', 'YEAR', 'WORKING_DAYS', 'del_ind'])

    calendar_details = django_query_instance.django_filter_query(CalenderConfig,
                                                                 {'del_ind': False}, None,
                                                                 ['calender_id', 'description', 'country_code', 'year',
                                                                  'working_days', 'del_ind'])
    calendar_details_data = query_update_del_ind(calendar_details)

    for calendar_detail in calendar_details_data:
        calendar_detail_info = [calendar_detail['calender_id'], calendar_detail['description'],
                                calendar_detail['country_code'], calendar_detail['year'],
                                calendar_detail['working_days'],
                                calendar_detail['del_ind']]
        writer.writerow(calendar_detail_info)

    return response


def extract_calendar_holiday_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_CALENDAR_HOLIDAY_CSV

    writer = csv.writer(response)
    writer.writerow(['CALENDER_ID', 'DESCRIPTION', 'COUNTRY_CODE', 'YEAR', 'del_ind'])

    calendar_holiday_details = django_query_instance.django_filter_query(CalenderConfig,
                                                                         {'del_ind': False}, None,
                                                                         ['calender_id', 'description', 'country_code',
                                                                          'year',
                                                                          'del_ind'])
    calendar_holiday_details_data = query_update_del_ind(calendar_holiday_details)

    for calendar_holiday_detail in calendar_holiday_details_data:
        calendar_holiday_detail_info = [calendar_holiday_detail['calender_id'], calendar_holiday_detail['description'],
                                        calendar_holiday_detail['country_code'], calendar_holiday_detail['year'],
                                        calendar_holiday_detail['del_ind']]
        writer.writerow(calendar_holiday_detail_info)

    return response


def extract_language_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Languages.CSV"'

    writer = csv.writer(response)
    writer.writerow(['LANGUAGE_ID', 'DESCRIPTION', 'del_ind'])

    # get only active records
    languages = django_query_instance.django_filter_query(Languages,
                                                          {'del_ind': False}, None,
                                                          ['language_id', 'description', 'del_ind'])
    language_data = query_update_del_ind(languages)

    for language in language_data:
        language_info = [language['language_id'], language['description'], language['del_ind']]
        writer.writerow(language_info)

    return response


def extract_language_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Languages Template.CSV"'

    writer = csv.writer(response)
    writer.writerow(['LANGUAGE_ID', 'DESCRIPTION', 'del_ind'])

    return response


def extract_currency_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_CURRENCY_CSV
    writer = csv.writer(response)

    writer.writerow(['CURRENCY_ID', 'DESCRIPTION', 'del_ind'])

    # get only active records
    currencies = django_query_instance.django_filter_query(Currency,
                                                           {'del_ind': False}, None,
                                                           ['currency_id', 'description', 'del_ind'])
    currency_data = query_update_del_ind(currencies)
    for currency in currency_data:
        currency_info = [currency['currency_id'], currency['description'], currency['del_ind']]
        writer.writerow(currency_info)

    return response


def srm_currency_converter_p02(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="filename.txt"'
    directory = os.path.join(str(settings.BASE_DIR), 'media', 'srm', 'currency')
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check for csv file
            if file.endswith(".csv") or file.endswith(".CSV"):
                file_path = os.path.join(directory, file)  # create path
                csv_file = open(file_path, 'r')  # open .csv file
                csvreader = csv.reader(csv_file)  # read file
                header = next(csvreader)  # skip header
                csv_to_db_data = []
                for csv_data in csvreader:
                    actual_data = csv_data[0].split('|')

                    # p02
                    currency_list = ['AED', 'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'DOP', 'EUR', 'GBP',
                                     'HKD', 'HRK', 'HUF', 'INR', 'ISK', 'JPY', 'KRW', 'KWD', 'LTL', 'LVL', 'MKD', 'MXN',
                                     'NOK', 'PLN', 'QAR', 'RON', 'RSD', 'RUB', 'SEK', 'SGD', 'SIT', 'SKK', 'TRY', 'UAH',
                                     'ZAR']
                    # E7P
                    # currency_list = ['AED','AUD','BGN','BRL','CAD','CHF','CNY','CZK','DKK','DOP','EUR','GBP','HKD','HUF',
                    #                  'INR','ISK','JPY','KRW','LTL','LVL','MKD','MXN','MYR','NOK','PLN','RMB','RON','RUB',
                    #                  'SEK','SGD','SIT','SKK','TRY','UAH','ZAR']
                    if actual_data[1] in currency_list:
                        usd_price = round(float(actual_data[4]), 5)
                        text = actual_data[1] + '\t' + 'USD' + '\t' + str(usd_price) + '\n'
                        response.write(text)
    return response


def srm_currency_converter_e7p(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="filename.txt"'
    directory = os.path.join(str(settings.BASE_DIR), 'media', 'srm', 'currency')
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check for csv file
            if file.endswith(".csv") or file.endswith(".CSV"):
                file_path = os.path.join(directory, file)  # create path
                csv_file = open(file_path, 'r')  # open .csv file
                csvreader = csv.reader(csv_file)  # read file
                header = next(csvreader)  # skip header
                csv_to_db_data = []
                for csv_data in csvreader:
                    actual_data = csv_data[0].split('|')
                    # E7P
                    currency_list = ['AED', 'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'DOP', 'EUR', 'GBP',
                                     'HKD', 'HUF',
                                     'INR', 'ISK', 'JPY', 'KRW', 'LTL', 'LVL', 'MKD', 'MXN', 'MYR', 'NOK', 'PLN', 'RMB',
                                     'RON', 'RUB',
                                     'SEK', 'SGD', 'SIT', 'SKK', 'TRY', 'UAH', 'ZAR']
                    if actual_data[1] in currency_list:
                        usd_price = round(float(actual_data[4]), 5)
                        text = actual_data[1] + '\t' + 'USD' + '\t' + str(usd_price) + '\n'
                        response.write(text)
    return response


def work_item_extract(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="filename.txt"'
    directory = os.path.join(str(settings.BASE_DIR), 'media', 'srm', 'workflow')
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check for csv file
            if file.endswith(".csv") or file.endswith(".CSV"):
                file_path = os.path.join(directory, file)  # create path
                csv_file = open(file_path, 'r')  # open .csv file
                csvreader = csv.reader(csv_file)  # read file
                header = next(csvreader)  # skip header
                csv_to_db_data = []
                for csv_data in csvreader:
                    actual_data = csv_data[0].split('|')
                    # doc num display
                    # doc_desc = actual_data[2].split('ID ')
                    # doc_num = doc_desc[1].split(' (GUID:')
                    # response.write(doc_num[0]+'\n')
                    # work item display
                    response.write(actual_data[0] + '\n')
    return response


def work_item_doc_num_extract(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="filename.txt"'
    directory = os.path.join(str(settings.BASE_DIR), 'media', 'srm', 'workflow')
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check for csv file
            if file.endswith(".csv") or file.endswith(".CSV"):
                file_path = os.path.join(directory, file)  # create path
                csv_file = open(file_path, 'r')  # open .csv file
                csvreader = csv.reader(csv_file)  # read file
                header = next(csvreader)  # skip header
                csv_to_db_data = []
                for csv_data in csvreader:
                    actual_data = csv_data[0].split('|')
                    # doc num display
                    doc_desc = actual_data[2].split('ID ')
                    doc_num = doc_desc[1].split(' (GUID:')
                    response.write(doc_num[0] + '\n')
    return response


def extract_timezone_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_TIMEZONE_CSV
    writer = csv.writer(response)
    writer.writerow(['TIME_ZONE', 'DESCRIPTION', 'UTC_DIFFERENCE', 'DAYLIGHT_SAVE_RULE', 'del_ind'])

    # get only active records
    timezones = django_query_instance.django_filter_query(TimeZone,
                                                          {'del_ind': False}, None,
                                                          ['time_zone', 'description', 'utc_difference',
                                                           'daylight_save_rule', 'del_ind'])
    timezone_data = query_update_del_ind(timezones)

    for timezone in timezone_data:
        timezone_info = [timezone['time_zone'], timezone['description'], timezone['utc_difference'],
                         timezone['daylight_save_rule'], timezone['del_ind']]
        writer.writerow(timezone_info)

    return response


def extract_workflowaccount_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Workflowacc.csv"'

    writer = csv.writer(response)

    writer.writerow(['ACC_VALUE', 'COMPANY_ID', 'APP_USERNAME', 'SUP_COMPANY_ID', 'SUP_ACC_VALUE',
                     'WORKFLOW_ACC_SOURCE_SYSTEM', 'ACCOUNT_ASSIGN_CAT', 'CLIENT', 'CURRENCY_ID',
                     'SUP_ACCOUNT_ASSIGN_CAT', 'DEL_IND'])

    # get only active records
    workflow_acct = django_query_instance.django_filter_query(WorkflowACC,
                                                              {'del_ind': False}, None,
                                                              ['acc_value', 'company_id', 'app_username',
                                                               'sup_company_id',
                                                               'sup_acc_value', 'workflow_acc_source_system',
                                                               'account_assign_cat',
                                                               'client', 'currency_id', 'sup_account_assign_cat',
                                                               'del_ind'])
    workflow_acct_data = query_update_del_ind(workflow_acct)

    for workflowacct in workflow_acct_data:
        workflowacct_info = [workflowacct['acc_value'], workflowacct['company_id'], workflowacct['app_username'],
                             workflowacct['sup_company_id'], workflowacct['sup_acc_value'],
                             workflowacct['workflow_acc_source_system'], workflowacct['account_assign_cat'],
                             workflowacct['client'], workflowacct['currency_id'],
                             workflowacct['sup_account_assign_cat'],
                             workflowacct['del_ind']]
        writer.writerow(workflowacct_info)

    return response


def extract_unitofmeasure_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Unit Of Measure.CSV"'

    writer = csv.writer(response)
    writer.writerow(['UOM_ID', 'UOM_DESCRIPTION', 'ISO_CODE_ID', 'del_ind'])
    # get only active records
    unitofmeasures = django_query_instance.django_filter_query(UnitOfMeasures,
                                                               {'del_ind': False}, None,
                                                               ['uom_id', 'uom_description', 'iso_code_id', 'del_ind'])
    unitofmeasure_data = query_update_del_ind(unitofmeasures)

    for unitofmeasure in unitofmeasure_data:
        unitofmeasure_info = [unitofmeasure['uom_id'], unitofmeasure['uom_description'], unitofmeasure['iso_code_id'],
                              unitofmeasure['del_ind']]
        writer.writerow(unitofmeasure_info)

    return response


def extract_unitofmeasure_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Unit Of Measure Template.CSV"'

    writer = csv.writer(response)
    writer.writerow(['UOM_ID', 'UOM_DESCRIPTION', 'ISO_CODE_ID', 'del_ind'])

    return response


def extract_product_details(request):
    update_user_info(request)
    # product_details = django_query_instance.django_filter_query(ProductsDetail,
    #                                                             {},None,None)
    # for product_detail in product_details:
    #     django_query_instance.django_update_query(ProductInfo,
    #                                               {'product_info_id':product_detail['product_info_id']},
    #                                               {'product_info_id':product_detail['product_id']})
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + CONST_PRODUCT_DETAIL_CSV

    writer = csv.writer(response)

    writer.writerow(
        ['ProductsDetail', 'PRODUCT_ID', 'SHORT_DESC', 'LONG_DESC', 'BUNDLE_FLAG', 'SUPP_PRODUCT_ID', 'SUPPLIER_ID',
         'SEARCH_TERM1', 'SEARCH_TERM2',
         'MANUFACTURER', 'BRAND', 'OFFER_KEY', 'PRICE_ON_REQUEST', 'MANU_PART_NUM', 'MANU_CODE_NUM',
         'PROD_TYPE', 'LEAD_TIME', 'QUANTITY_AVAIL', 'GROSS_PRICE', 'PRICE_UNIT', 'CUST_PROD_CAT_ID', 'QUANTITY_MIN',
         'VALUE_MIN', 'QUANTITY_MAX', 'TIERED_FLAG', 'CTR_NUM', 'CTR_ITEM_NUM', 'CTR_NAME',
         'PRODUCT_STATUS', 'SGST', 'CGST', 'VAT', 'PRICE_1', 'QUANTITY_1', 'PRICE_2', 'QUANTITY_2', 'PRICE_3',
         'QUANTITY_3', 'EXTERNAL_LINK', 'SUPPLIER_PRODUCT_INFO', 'EFORM_ID', 'PRODUCT_INFO_ID', 'COUNTRY_OF_ORIGIN',
         'CURRENCY', 'LANGUAGE', 'PROD_CAT_ID', 'UNIT_OF_MEASURE',
         'del_ind', 'PRODUCT_IMAGE_PATH'])
    writer.writerow(
        ['ProductSpecification', 'product_info_id', 'product_info_key', 'product_info_value', 'del_ind'])

    products = ProductsDetail.objects.filter(client=global_variables.GLOBAL_CLIENT).values('product_id', 'short_desc',
                                                                                           'long_desc', 'bundle_flag',
                                                                                           'supp_product_id',
                                                                                           'supplier_id',
                                                                                           'search_term1',
                                                                                           'search_term2',
                                                                                           'manufacturer', 'brand',
                                                                                           'offer_key',
                                                                                           'price_on_request',
                                                                                           'manu_part_num',
                                                                                           'manu_code_num',
                                                                                           'prod_type', 'lead_time',
                                                                                           'quantity_avail', 'price',
                                                                                           'price_unit',
                                                                                           'cust_prod_cat_id',
                                                                                           'quantity_min',
                                                                                           'value_min', 'quantity_max',
                                                                                           'tiered_flag', 'ctr_num',
                                                                                           'ctr_item_num', 'ctr_name',
                                                                                           'product_status', 'sgst',
                                                                                           'cgst', 'vat', 'price_1',
                                                                                           'quantity_1', 'price_2',
                                                                                           'quantity_2', 'price_3',
                                                                                           'quantity_3',
                                                                                           'external_link',
                                                                                           'supplier_product_info',
                                                                                           'eform_id',
                                                                                           'product_info_id',
                                                                                           'country_of_origin',
                                                                                           'currency', 'language',
                                                                                           'prod_cat_id', 'unit',
                                                                                           'del_ind')
    filter_queue = ~Q(product_info_id=None)
    product_id_list = django_query_instance.django_queue_query_value_list(ProductsDetail,
                                                                          {'client': global_variables.GLOBAL_CLIENT,
                                                                           },
                                                                          filter_queue,
                                                                          'product_id')

    product_spec_details = django_query_instance.django_filter_query(ProductInfo,
                                                                     {'client': global_variables.GLOBAL_CLIENT,
                                                                      'product_info_id__in': product_id_list},
                                                                     None, None)
    prod_id_list_spec = django_query_instance.django_filter_value_list_query(ProductInfo,
                                                                             {'client': global_variables.GLOBAL_CLIENT,
                                                                              'product_info_id__in': product_id_list},
                                                                             'product_info_id')
    prod_data = update_del_ind(products)
    # print(prod_data)

    for prod in prod_data:
        prod.insert(0, 'ProductsDetail')
        prod.append(None)
        writer.writerow(prod)
        if prod[1] in prod_id_list_spec:
            for product_spec_detail in product_spec_details:
                if product_spec_detail['product_info_id'] == prod[1]:
                    writer.writerow(['ProductSpecification',
                                     product_spec_detail['product_info_id'],
                                     product_spec_detail['product_info_key'],
                                     product_spec_detail['product_info_value'],
                                     product_spec_detail['del_ind']])

    return response


def download_product_template(request):
    """

    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + CONST_PRODUCT_DETAIL_TEMPLATE_CSV

    writer = csv.writer(response)

    writer.writerow(
        ['PRODUCT_ID', 'SHORT_DESC', 'LONG_DESC', 'BUNDLE_FLAG', 'SUPP_PRODUCT_ID', 'SUPPLIER_ID', 'SEARCH_TERM1',
         'SEARCH_TERM2',
         'MANUFACTURER', 'BRAND', 'OFFER_KEY', 'PRICE_ON_REQUEST', 'MANU_PART_NUM', 'MANU_CODE_NUM',
         'PROD_TYPE', 'LEAD_TIME', 'QUANTITY_AVAIL', 'GROSS_PRICE', 'PRICE_UNIT', 'CUST_PROD_CAT_ID', 'QUANTITY_MIN',
         'VALUE_MIN', 'QUANTITY_MAX', 'TIERED_FLAG', 'CTR_NUM', 'CTR_ITEM_NUM', 'CTR_NAME',
         'PRODUCT_STATUS', 'SGST', 'CGST', 'VAT', 'PRICE_1', 'QUANTITY_1', 'PRICE_2', 'QUANTITY_2', 'PRICE_3',
         'QUANTITY_3', 'EXTERNAL_LINK', 'SUPPLIER_PRODUCT_INFO', 'EFORM_ID', 'PRODUCT_INFO_ID', 'COUNTRY_OF_ORIGIN',
         'CURRENCY', 'LANGUAGE', 'PROD_CAT_ID', 'UNIT_OF_MEASURE',
         'del_ind', 'PRODUCT_IMAGE_PATH'])
    writer.writerow(
        ['ProductSpecification', 'product_info_id', 'product_info_key', 'product_info_value', 'del_ind'])

    return response


def upload_cust_prod_cat(request):
    client = getClients(request)
    upload_cust_prod_catogories = get_configuration_data(
        UnspscCategoriesCust, {'client': client, 'del_ind': False}, ['prod_cat_guid', 'prod_cat_id'])

    content_managment_settings = 'content_managment_settings'
    return render(request,
                  'Customer_Product_Category/customer_product_category.html',
                  {'upload_cust_prod_cat': upload_cust_prod_catogories,
                   'content_managment_settings': content_managment_settings
                   })


def upload_cust_prod_cat_desc(request):
    client = getClients(request)

    upload_cust_prod_desc_catogories = get_configuration_data(
        UnspscCategoriesCustDesc, {'client': client, 'del_ind': False}, ['prod_cat_desc_guid',
                                                                         'prod_cat_id',
                                                                         'category_desc', 'language_id'])
    content_managment_settings = 'content_managment_settings'
    return render(request,
                  'Customer_Product_Category_Descriptiony/customer_product_category_description.html',
                  {'upload_cust_prod_cat_desc': upload_cust_prod_desc_catogories,
                   'content_managment_settings': content_managment_settings
                   })


# upload_ProdCat = list(UnspscCategories.objects.filter(del_ind=False).values('prod_cat_id', 'prod_cat_desc'))

# for prod_cat_desc in upload_ProdCat:

#   if prod_cat_desc['prod_cat_desc'] == None:
#      prod_cat_desc['prod_cat_desc'] = ''

# basic_settings = 'basic_settings'
# DB_count = UnspscCategories.objects.filter(del_ind=False).count()
# return render(request, 'Basic_setting_Upload/upload_product_category.html',
#             {'upload_product_category': upload_ProdCat, 'basic_settings': basic_settings, 'DB_count': DB_count,
#             'inc_nav': True})


def upload_timezone(request):
    upload_timezones = get_configuration_data(TimeZone, {'del_ind': False},
                                              ['time_zone', 'description', 'utc_difference',
                                               'daylight_save_rule'])
    return render(request, 'Basic_setting_Upload/upload_timezone.html',
                  {'upload_timezone': upload_timezones,
                   'inc_nav': True})


def account_ass_values(request):
    upload_accassvalues = get_configuration_data(AccountingData, {'del_ind': False},
                                                 ['account_assign_guid', 'account_assign_value', 'valid_from',
                                                  'valid_to', 'account_assign_cat', 'company_id'])
    upload_data_acccat = get_configuration_data(AccountAssignmentCategory, {'del_ind': False}, ['account_assign_cat'])
    upload_data_company = get_configuration_data(OrgCompanies, {'del_ind': False}, ['company_id'])
    master_data_settings = 'master_data_settings'
    for data in upload_accassvalues:
        print(data)
    return render(request, 'Accounting_Data/account_assignment_values.html',
                  {'account_ass_values': upload_accassvalues, 'upload_data_acccat': upload_data_acccat,
                   'upload_data_company': upload_data_company, 'master_data_settings': master_data_settings,
                   'inc_nav': True})


def purch_Cockpit(request):
    client = getClients(request)
    upload_purchcockpit = list(
        purch_cockpit.objects.filter(client=client, del_ind=False).values('guid', 'from_prod_cat', 'to_prod_cat',
                                                                          'purch_cockpit_value'))
    purchase_data_settings = 'purchase_data_settings'
    return render(request, 'Purchaser_Cockpit/purchase_cockpit.html',
                  {'purch_Cockpit': upload_purchcockpit, 'purchase_data_settings': purchase_data_settings})


def upload_catalog(request):
    client = getClients(request)
    my_list = CatalogManagement.get_catalogs_not_used()
    upload_catalog = list(
        Catalogs.objects.filter(client=client, del_ind=False).values('catalog_guid', 'catalog_id', 'name',
                                                                     'description', 'product_type'))
    content_managment_settings = 'content_managment_settings'
    return render(request, 'Content_Managment_new/upload_catalog.html',
                  {'upload_catalog': upload_catalog, 'my_list': my_list,
                   'content_managment_settings': content_managment_settings})


def upload_product_cattegories(request):
    client = getClients(request)
    upload_pcattegories = list(
        ProductsDetail.objects.filter(client=client, del_ind=False).values('product_id', 'short_desc', 'supplier_id',
                                                                           'lead_time', 'unit', 'price', 'currency',
                                                                           'long_desc', 'catalog_item', 'catalog_id',
                                                                           'product_type', 'price_on_request',
                                                                           'price_unit', 'manufacturer',
                                                                           'manu_part_num',
                                                                           'brand', 'quantity_avail', 'quantity_min',
                                                                           'offer_key', 'country_of_origin', 'language',
                                                                           'cust_prod_cat_id', 'search_term1',
                                                                           'search_term2',
                                                                           'prod_cat_id'))
    supp_data = list(
        SupplierMaster.objects.filter(client=global_variables.GLOBAL_CLIENT, del_ind=False).values('supplier_id',
                                                                                                   'name1'))
    get_units = list(UnitOfMeasures.objects.filter(del_ind=False).values('uom_id', 'uom_description'))
    currency_list = list(Currency.objects.filter(del_ind=False).values('currency_id', 'description'))
    country_list = list(Country.objects.filter(del_ind=False).values('country_code', 'country_name'))
    language_list = list(Languages.objects.filter(del_ind=False).values('language_id', 'description'))
    catalogs_list = list(CatalogGenericMethods.catalog_list())
    unspsc_list = list(UnspscCategoriesCustDesc.objects.filter(del_ind=False).values('prod_cat_id', 'category_desc'))

    content_managment_settings = 'content_managment_settings'
    return render(request, 'Content_Managment_new/upload_product_cattegories.html',
                  {'upload_product_cattegories': upload_pcattegories, 'supp_data': supp_data, 'get_units': get_units,
                   'currency_list': currency_list, 'country_list': country_list, 'language_list': language_list,
                   'unspsc_list': unspsc_list, 'catalogs_list': catalogs_list,
                   'content_managment_settings': content_managment_settings,
                   })


# def upload_cust_prod_cat(request):
#     client = getClients(request)
#     upload_cust_prod_catogories = list(
#         UnspscCategoriesCust.objects.filter(client=client, del_ind=False).values('prod_cat_guid', 'prod_cat_id'))
#     content_managment_settings = 'content_managment_settings'
#     return render(request,
#                   'Customer_Product_Category/customer_product_category.html',
#                   {'upload_cust_prod_cat': upload_cust_prod_catogories,
#                    'content_managment_settings': content_managment_settings
#                    })
#
#
# def upload_cust_prod_cat_desc(request):
#     client = getClients(request)
#     upload_cust_prod_desc_catogories = list(
#         UnspscCategoriesCustDesc.objects.filter(client=client, del_ind=False).values('prod_cat_desc_guid',
#                                                                                      'prod_cat_id',
#                                                                                      'category_desc', 'language_id'))
#     content_managment_settings = 'content_managment_settings'
#     return render(request,
#                   'Customer_Product_Category_Descriptiony/customer_product_category_description.html',
#                   {'upload_cust_prod_cat_desc': upload_cust_prod_desc_catogories,
#                    'content_managment_settings': content_managment_settings
#                    })


def check_data(request):
    if request.is_ajax():
        # retrieving data_list, Tablename, appname,db_header_data from UI
        table_data__array = JsonParser_obj.get_json_from_req(request)
        popup_data_list = table_data__array['data_list']
        db_header_data = table_data__array['db_header_data']
        check_data_class = UploadBasicTables(request)
        check_data_class.app_name = table_data__array['appname']
        check_data_class.table_name = table_data__array['Tablename']
        # gets he count from basic_table_new_conditions() - upload_pk_tables.py
        check_variable = check_data_class.basic_table_new_conditions(popup_data_list, db_header_data)
        print("check", check_variable)
        return JsonResponse(check_variable, safe=False)

    return render(request, 'Basic_setting_Upload/upload_countries.html')


def extract_employee_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="EMPLOYEE.CSV"'

    writer = csv.writer(response)

    writer.writerow(
        ['EMAIL', 'USERNAME', 'PERSON_NO', 'FORM_OF_ADDRESS', 'FIRST_NAME', 'LAST_NAME', 'PHONE_NUM', 'PASSWORD',
         'DATE_JOINED', 'FIRST_LOGIN', 'LAST_LOGIN', 'IS_ACTIVE', 'IS_SUPERUSER', 'IS_STAFF', 'DATE_FORMAT',
         'EMPLOYEE_ID', 'DECIMAL_NOTATION', 'USER_TYPE', 'LOGIN_ATTEMPTS', 'USER_LOCKED', 'PWD_LOCKED', 'SSO_USER',
         'VALID_FROM', 'VALID_TO', 'del_ind', 'CURRENCY_ID', 'LANGUAGE_ID', 'OBJECT_ID', 'TIME_ZONE'])
    # get only active record
    emp = django_query_instance.django_filter_query(UserData,
                                                    {'del_ind': False}, None,
                                                    ['email', 'username', 'person_no', 'form_of_address',
                                                     'first_name', 'last_name', 'phone_num', 'password',
                                                     'date_joined', 'first_login', 'last_login', 'is_active',
                                                     'is_superuser', 'is_staff', 'date_format',
                                                     'employee_id', 'decimal_notation', 'user_type',
                                                     'login_attempts', 'user_locked', 'pwd_locked', 'sso_user',
                                                     'valid_from', 'valid_to', 'del_ind', 'currency_id', 'language_id',
                                                     'object_id', 'time_zone'])
    emp_data = query_update_del_ind(emp)

    for employee in emp_data:
        emp_info = [employee['email'], employee['username'], employee['person_no'], employee['form_of_address'],
                    employee['first_name'], employee['last_name'], employee['phone_num'], employee['password'],
                    employee['date_joined'], employee['first_login'], employee['last_login'], employee['is_active'],
                    employee['is_superuser'], employee['is_staff'], employee['date_format'],
                    employee['employee_id'], employee['decimal_notation'], employee['user_type'],
                    employee['login_attempts'], employee['user_locked'], employee['pwd_locked'], employee['sso_user'],
                    employee['valid_from'], employee['valid_to'], employee['del_ind'], employee['currency_id'],
                    employee['language_id'],
                    employee['object_id'], employee['time_zone']]
        writer.writerow(emp_info)

    return response


scheduler = BackgroundScheduler()

def Scheduling(request):
    """

    """

    scheduler.add_job(train_model, 'interval', seconds=3, id='my_job_id')
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
    context = {}
    return render(request, 'Application_Settings/srm_currency.html', context)


def train_model():
    print('dask train_model! The time is: %s' % datetime.now())


def stop_job(request):
    """

    """

    scheduler.remove_job('my_job_id')
    context = {}
    return render(request, 'Application_Settings/srm_currency.html', context)
