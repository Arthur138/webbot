from datetime import datetime

from fast_bitrix24 import Bitrix, BitrixAsync
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from adrf.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from webbot.utils import process_and_save_address_data
from django.http import JsonResponse
from webbot.forms import AddressForm
from webbot.models import Location
from webbot.serializers import LocationSerializer
from telegraph import Telegraph
from rest_framework.parsers import MultiPartParser, FormParser
import json
import asyncio
import requests
import time
from venv import logger
import sys
from http import HTTPStatus
from urllib import parse as urllib_parse
import cx_Oracle



async def contact_registr(name, lastname, mobile, mobile2):
    webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
    b = Bitrix(webhook)
    method = 'crm.contact.add'
    params = {'fields': {
        'NAME': name,
        'LAST_NAME': lastname,
        'ASSIGNED_BY_ID': 87,
        'PHONE': [{"VALUE": mobile, "VALUE_TYPE": "WORK"}, {"VALUE": mobile2, "VALUE_TYPE": "WORK"}],
    }}
    response = await b.call(method, params)
    return response

async def contact_ls(n_subject_id,hydra_ls,contact_id,adress_abon):
    webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
    b = BitrixAsync(webhook)
    method = 'crm.contact.update'
    params = {
            'ID': f'{contact_id}',
            'fields': {
                'UF_CRM_1687325219482': f'{hydra_ls}',
                'UF_CRM_1674820632467': f'{n_subject_id}',
                'UF_CRM_1687325330978': f'{adress_abon}'
            }
    }
    test = await b.call(method, params)
    return test

async def application_internet(bx_region, bx_district, bx_order_status, bx_router, bx_tariff, bx_tv,
                               bx_provider_from, description,
                               userAdditionalPhoneNumber, address, passport1, passport2,
                               location_screenshot, region_path_id, contact_id):
    webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
    b = Bitrix(webhook)
    method = 'crm.deal.add'
    test = {'fields': {
        'TITLE': 'Заявка на интернет',
        'TYPE_ID': 6667,

        'UF_CRM_1674993837284': bx_district,
        'UF_CRM_1673408541': location_screenshot,  # ссылка на локацию ^^
        'UF_CRM_1673408700': passport1,  # ссылка на пасспорт ^^
        'UF_CRM_1673408725': passport2,  # Ссылка  на   паспорт2 ^^
        'UF_CRM_1669625413673': bx_region,  # области  Иссык-Кульская
        'UF_CRM_1673255771': userAdditionalPhoneNumber,  # Лицевой счет **
        'UF_CRM_1673258743852': description,  # описание заявки ^^
        'UF_CRM_1669634833014': bx_router,  # Роутер ^^
        'UF_CRM_1669625771519': bx_tariff,  # Тариф ^^
        'UF_CRM_1669625805213': bx_tv,  # ТВ ^^
        'UF_CRM_1673251826': bx_order_status,  # Статус оплаты ^^
        'UF_CRM_1673251960': bx_provider_from,  # Переход от  какого провайдера ^^
        'UF_CRM_1695971054382': bx_district,  # Лицевой  счет УР ^^
        'CATEGORY_ID': region_path_id,
        'CONTACT_ID': contact_id
    }}
    test2 = await b.call(method, test, raw=False)
    print(test2)
    return test2




class Zayavka(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print('---------')
        user = request.user
        print(user)
        print('---------')

        bx_region = data.get('region2', 'Значение по умолчанию').get('ID', 'Значение по умолчанию')
        bx_region_value = data.get('region2', 'Значение по умолчанию').get('VALUE', 'Значение по умолчанию')
        bx_district = data.get('district2', 'Значение по умолчанию').get('VALUE', 'Значение по умолчанию')
        bx_order_status = data.get('orderStatus', 'Значение по умолчанию').get('ID', 'Значение по умолчанию')
        bx_router = data.get('routerInstallationType', 'Значение по умолчанию').get('ID', 'Значение по умолчанию')
        bx_tariff = data.get('tariff', 'Значение по умолчанию').get('ID', 'Значение по умолчанию')
        bx_tv = data.get('superTv', 'Значение по умолчанию').get('ID', 'Значение по умолчанию')
        bx_provider_from = data.get('providerFrom', 'Значение по умолчанию').get('ID', 'Значение по умолчанию')
        description = data.get('description', 'Значение по умолчанию')
        username = data.get('username', 'Значение по умолчанию')
        userSirName = data.get('userSirName', 'Значение по умолчанию')
        userPhoneNumber = data.get('userPhoneNumber', 'Значение по умолчанию')
        userAdditionalPhoneNumber = data.get('userAdditionalPhoneNumber', 'Значение по умолчанию')
        address = data.get('address', 'Значение по умолчанию')
        hydra_region_id = address.get('region', 'Значение по умолчанию').get('hydra_id', 'Значение по умолчанию')
        last_key = list(address.keys())[-1]
        last_value = address[last_key]
        hydra_address = last_value['hydra_id']
        exactaddress = data.get('exactAddress', 'Значение по умолчанию').get('address', 'Значение по умолчанию')
        passport1 = data.get('assets', 'Значение по умолчанию').get('passport1', 'Значение по умолчанию')
        passport2 = data.get('assets', 'Значение по умолчанию').get('passport2', 'Значение по умолчанию')
        location_screenshot = data.get('assets', 'Значение по умолчанию').get('locationScreenShot', 'Значение по умолчанию')

        contact_id = asyncio.run(
            contact_registr(username, userSirName, userPhoneNumber, userAdditionalPhoneNumber ))
        print('----------------')
        print(contact_id)
        print('----------------')

        region_id_mapping = {
            'Иссык-Кульская': 29,
            'Джалал-Абадская': 33,
            'Таласская': 30,
            'Нарынская': 31,
            'Чуйская': 23,
            'Ошская': 32,
        }
        region_path_id = region_id_mapping[bx_region_value]
        bx_id = asyncio.run(application_internet(
            bx_region, bx_district, bx_order_status, bx_router, bx_tariff, bx_tv,
            bx_provider_from, description,
            userAdditionalPhoneNumber, address , passport1 , passport2 , location_screenshot,region_path_id, contact_id
        ))
        print('----------------')
        print(bx_id)
        print('----------------')

        hoper_url = 'https://hydra.snt.kg:8000/rest/v2/'
        hoper_login = 'skybot'
        hoper_password = '*hjvfirf!'
        http_timeout = 60
        http_session = requests.Session()
        http_session.headers.update(
            {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )
        auth_url = urllib_parse.urljoin(hoper_url, 'login')
        print(auth_url)
        auth_params = {'session': {'login': hoper_login, 'password': hoper_password}}
        response = http_session.post(
            auth_url,
            timeout=http_timeout,
            json=auth_params,
            verify=False,
        )

        if response.status_code != HTTPStatus.CREATED:
            logger.error(
                'Auth error ({0}): {1}'.format(response.status_code, response.content),
            )
            sys.exit(1)
        logger.debug(response.content)

        auth_result = json.loads(response.content)
        auth_token = auth_result['session']['token']
        print(auth_token)

        http_session.headers.update(
            {'Authorization': 'Token token={0}'.format(auth_token)},
        )

        organizations_url = urllib_parse.urljoin(hoper_url, 'subjects/persons/')
        response = http_session.post(
            organizations_url,
            timeout=http_timeout,
            json={
                "person": {
                    "vc_first_name": f"{username}",
                    "vc_surname": f"{userSirName}",
                    'n_subj_state_id': 2011,
                    "vc_second_name": "",
                    "vc_rem": "Физ.лицо создан через Бота",
                }
            }
        )

        if response.status_code == 201:
            search_results = json.loads(response.content)
            print("fizlico")
            print(search_results)

            if hydra_region_id == 51385501:
                n_reseller_id = 7992244901
            elif hydra_region_id == 51386001:
                n_reseller_id = 7992055601
            elif hydra_region_id == 51385801:
                n_reseller_id = 7992052401
            elif hydra_region_id == 51386201:
                n_reseller_id = 7992041401
            elif hydra_region_id == 51385601:
                n_reseller_id = 7991945001
            elif hydra_region_id == 51386101:
                n_reseller_id = 7992048101

            print(search_results['person']['n_person_id'])
            n_person_id = search_results['person']['n_person_id']
            # Core_to_hydra.objects.filter(bitrix_deal_id=bitrix_deal_id).update(n_person_id=n_person_id)
            organizations_url = urllib_parse.urljoin(hoper_url, 'subjects/customers/')
            response = http_session.post(
                organizations_url,
                timeout=http_timeout,
                json={
                    "customer": {

                        "n_base_subject_id": n_person_id,
                        'n_base_subj_type_id': 18001,
                        'n_subj_state_id': 2011,
                        "n_subj_group_id": 51207501,
                        'n_reseller_id': n_reseller_id,
                        "group_ids": [
                            40231101
                        ],

                    }
                }
            )
            # ls  f"'{message.text}'"
            print(response.status_code)
            if response.status_code == 201:
                search_results = json.loads(response.content)
                print("abon")
                print(search_results)

                n_subject_id = search_results['customer']['n_subject_id']
                # Core_to_hydra.objects.filter(bitrix_deal_id=bitrix_deal_id).update(n_customer_id=n_subject_id)
                organizations_url = urllib_parse.urljoin(hoper_url, f"subjects/customers/{n_subject_id}/accounts")
                # time.sleep(1)
                response = http_session.post(
                    organizations_url,
                    timeout=http_timeout,
                    json={
                        "account": {
                            "n_currency_id": 7044,
                            'vc_currency_code': 'KGS',

                        }
                    }
                )
                print(response.status_code)
                if response.status_code == 201:
                    search_results = json.loads(response.content)
                    print("ls")
                    print(search_results)

                    hydra_ls = search_results['account']['vc_code']
                    hydra_ls_code = search_results['account']['n_account_id']
                    print(hydra_ls)
                    # Core_to_hydra.objects.filter(bitrix_deal_id=bitrix_deal_id).update(n_account_id=hydra_ls_code)

                    # requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token),
                    #              params=dict(chat_id=tg_id, text=('Лицевой  счет №:' + hydra_ls + '\n')
                    #                          ))

                    # Core_to_hydra.objects.filter(bitrix_deal_id=bitrix_deal_id).update(hydra_ls=hydra_ls)

                    organizations_url = urllib_parse.urljoin(hoper_url, f"subjects/customers/{n_subject_id}/")
                    response = http_session.put(
                        organizations_url,
                        timeout=http_timeout,
                        json=
                        {
                            "customer": {

                                'additional_values':
                                    [{'code': 'Продавец', 'name': 'Продавец', 'value': f"hydra.hydra_id_sales"}]
                                #hydra.hydra_id_sales = агент
                            }
                        }

                    )
                    print(response.status_code)

                    if response.status_code == 200:
                        search_results = json.loads(response.content)
                        print("dogovor")
                        print(search_results)
                        link = f'https://hydra.snt.kg:8000/subjects/persons/edit/{n_person_id}'
                        organizations_url = urllib_parse.urljoin(hoper_url,
                                                                 f"subjects/customers/{n_subject_id}/contracts")
                        response = http_session.post(
                            organizations_url,
                            timeout=http_timeout,
                            json=
                            {
                                "contract": {
                                    "n_doc_type_id": 1002,
                                    'n_doc_state_id': 4003,
                                    "n_workflow_id": 10021,
                                    "n_parent_doc_id": 40232501,
                                    "n_provider_id": 100,
                                    "n_firm_id": 100,

                                }
                            }

                        )
                        search_results = json.loads(response.content)
                        print("dogovor active")
                        print(search_results)
                        n_contract_id = search_results['contract']['n_doc_id']
                        hydra_ls_doc = search_results['contract']['vc_doc_no']
                        # requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token),
                        #              params=dict(chat_id=f"{hydra.tg_id}", text=(' Договор №:' + hydra_ls_doc + '\n')
                        #                          ))
                        #
                        # Core_to_hydra.objects.filter(bitrix_deal_id=bitrix_deal_id).update(n_contract_id=n_contract_id)

                        organizations_url = urllib_parse.urljoin(hoper_url,
                                                                 f'subjects/customers/{n_subject_id}/contracts/{n_contract_id}')
                        response = http_session.put(
                            organizations_url,
                            timeout=http_timeout,
                            json=
                            {
                                "contract": {

                                    'n_doc_state_id': 4003,

                                }
                            }

                        )
                        if response.status_code == 200:
                            search_results = json.loads(response.content)

                            organizations_url = urllib_parse.urljoin(hoper_url,
                                                                     f"subjects/persons/{n_person_id}/addresses/")
                            print(organizations_url)
                            response = http_session.post(
                                organizations_url,
                                timeout=http_timeout,
                                json=
                                {
                                    "address": {
                                        "n_addr_type_id": 13006,
                                        'vc_code': f"{userAdditionalPhoneNumber}",
                                        'n_subj_addr_type_id': 9016,
                                        'n_addr_state_id': 1029,

                                    }
                                }

                            )
                            print(response)
                            if response.status_code == 201:
                                search_results = json.loads(response.content)
                                print("ls")
                                print(search_results)

                                organizations_url = urllib_parse.urljoin(hoper_url,
                                                                         f"subjects/persons/{n_person_id}/addresses/")
                                response = http_session.post(
                                    organizations_url,
                                    timeout=http_timeout,
                                    json=
                                    {
                                        "address": {
                                            "n_addr_type_id": 13006,
                                            'vc_code': f"{userPhoneNumber}",
                                            'n_subj_addr_type_id': 12016,
                                            'n_addr_state_id': 1029,

                                        }
                                    }

                                )
                                # adres
                                if response.status_code == 201:
                                    search_results = json.loads(response.content)
                                    print("tel")
                                    print(search_results)

                                    dsn = cx_Oracle.makedsn(host='hydra.snt.kg', port='1521', service_name='hydra')
                                    # Establish the database connection
                                    dbh = cx_Oracle.connect(user='AIS_NET',
                                                            password='AeFae0eeleatohraelah',
                                                            dsn=dsn
                                                            )

                                    with dbh.cursor() as cursor:
                                        v_region_id = cursor.var(cx_Oracle.NUMBER)
                                        cv_region_id = cursor.var(cx_Oracle.NUMBER)
                                        cursor.execute("""
                                                BEGIN
                                                    SR_REGIONS_PKG.SR_REGIONS_PUT(
                                                        num_N_REGION_ID => :v_region_id,
                                                        num_N_REGION_TYPE_ID => :region_type_id,
                                                        num_N_PAR_REGION_ID => :par_region_id,
                                                        vch_VC_CODE => :vc_code,
                                                        vch_VC_NAME => :vc_name,
                                                        vch_VC_ENG_NAME => :vc_eng_name,
                                                        num_N_HIERARCHY_TYPE_ID => :hierarchy_type_id,
                                                        num_N_BASE_REGION_ID => :base_region_id,
                                                        num_N_PAR_BIND_REGION_ID => :par_bind_region_id,
                                                        num_N_REALTY_GOOD_ID => :realty_good_id,
                                                        vch_VC_ZIP => :vc_zip,
                                                        vch_VC_HOME => :vc_home,
                                                        vch_VC_BUILDING => :vc_building,
                                                        vch_VC_CONSTRUCT => :vc_construct,
                                                        vch_VC_OWNERSHIP => :vc_ownership,
                                                        vch_VC_CODE_EXT => :vc_code_ext,
                                                        b_UpdateSearchIndex => :update_search_index
                                                    );
                                                END;
                                            """, v_region_id=v_region_id,
                                                       region_type_id=6027,
                                                       par_region_id=hydra_address,
                                                       vc_code=None,
                                                       vc_name=None,
                                                       vc_eng_name=None,
                                                       hierarchy_type_id=1037,
                                                       base_region_id=None,
                                                       par_bind_region_id=None,
                                                       realty_good_id=None,
                                                       vc_zip=None,
                                                       vc_home=exactaddress,
                                                       vc_building=None,
                                                       vc_construct=None,
                                                       vc_ownership=None,
                                                       vc_code_ext=None,
                                                       update_search_index=None
                                                       )

                                        dbh.commit()
                                        region_id_value = int(v_region_id.getvalue())
                                        print(f"Создана улица с ID: {region_id_value}")
                                        abon_address_full = cursor.callfunc("SR_REGIONS_PKG_S.GET_VISUAL_CODE", cx_Oracle.STRING,
                                                                      [region_id_value])
                                        print(f'{abon_address_full}')
                                    dbh.close()

                                    organizations_url = urllib_parse.urljoin(hoper_url,
                                                                             f"subjects/persons/{n_person_id}/addresses/")
                                    # adress_abon = f"{hydra.ticket_location} {hydra.ticket_adress}"
                                    response = http_session.post(
                                        organizations_url,
                                        timeout=http_timeout,
                                        json=
                                        {

                                            "address": {
                                                "n_addr_type_id": 1006,
                                                "n_subj_addr_type_id": 1016,
                                                "n_region_id": region_id_value,
                                                "vc_rem": "Необходимо  уточнить",
                                                "n_addr_state_id": 1029
                                            }
                                        }

                                    )

                                    print(response.status_code)
                                    if response.status_code == 201:
                                        search_results = json.loads(response.content)
                                        print(search_results)

                                    now = datetime.now()
                                    time = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
                                    organizations_url = urllib_parse.urljoin(hoper_url,
                                                                             f"subjects/customers/{n_subject_id}/comments/")
                                    asyncio.run(contact_ls(n_subject_id, hydra_ls, contact_id, abon_address_full))
                                    response = http_session.post(
                                        organizations_url,
                                        timeout=http_timeout,
                                        json=
                                        {

                                            "comment": {
                                                "n_comment_type_id": 2082,
                                                'd_oper': f'{time}',
                                                "cl_comment": f" Ссылка на заявку: http://bitrix24.snt.kg/crm/deal/details/{bx_id}/        UR ls - lsdom",

                                                "n_author_id": 3778825901
                                            }
                                        }

                                    )
        return Response({"message": "Данные получены"}, status=200)

class Bx_router(APIView):
    def get(self, request):
        fields_list = ['UF_CRM_1669625413673','UF_CRM_1669625771519', 'UF_CRM_1669634833014', 'UF_CRM_1673251826', 'UF_CRM_1673251960', 'UF_CRM_1669625805213','UF_CRM_1669625805213']
        webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
        response_data = []
        for field in fields_list:
            response = requests.get(f'{webhook}crm.deal.fields')  
            if response.status_code == 200:
                fields_info = response.json()
                for id_field, field_value in fields_info.get('result', {}).items():
                    if field in id_field and field_value['type'] == 'enumeration':
                        items = field_value['items']
                        response_data.append(items)
        # print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)


class UploadPassportView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        telegraph = Telegraph(access_token="340810480920e8986d089f2d8b5f55abd26da83d3ea8ae78db100d70946a")

        responses = []
        for i in range(1, 4):  # Обработка трех файлов
            file_key = f'file{i}'
            file = request.FILES.get(file_key)
            if file:
                try:
                    response = self.upload_and_create_page(file, telegraph, f'Passport Image {i}')
                    responses.append(response)
                except Exception as e:
                    return Response({'message': f'Failed to upload {file_key}: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': f'{file_key} is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Формирование итогового ответа
        return Response({
            'message': 'Images uploaded successfully',
            'data': responses
        }, status=status.HTTP_200_OK)

    def upload_and_create_page(self, file, telegraph, title):
        response = requests.post(
            'https://telegra.ph/upload',
            files={'file': (file.name, file, file.content_type)}
        )
        if response.status_code == 200:
            path = response.json()[0]['src']
            full_path = f'https://telegra.ph{path}'

            page_response = telegraph.create_page(
                title=title,
                html_content=f"<p>{title}</p><img src='{full_path}'/>"
            )
            page_url = f'https://telegra.ph/{page_response["path"]}'
            return {'title': title, 'image_path': full_path, 'page_url': page_url}
        else:
            raise Exception('Failed to upload image to Telegraph')


class bx(APIView):
    def get(self, request):
        fields_list = ['UF_CRM_1675072231', 'UF_CRM_1675071171', 'UF_CRM_1675070693', 'UF_CRM_1675071012', 'UF_CRM_1675070436', 'UF_CRM_1675071353' ]
        webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
        response_data = {}
        region_mapping = {
        'Чуй':'UF_CRM_1675072231',
        'Иссык-Куль': 'UF_CRM_1675071171',
        'Ош': 'UF_CRM_1675070693',
        'Нарын': 'UF_CRM_1675071012',
        'Талас': 'UF_CRM_1675070436',
        'Джалал-Абад': 'UF_CRM_1675071353'
        }
        response = requests.get(f'{webhook}crm.deal.fields')
        if response.status_code == 200:
            fields_info = response.json().get('result', {})
            for field in fields_list:
                field_value = fields_info.get(field)
                if field_value and field_value['type'] == 'enumeration':
                    items = field_value['items']
                    region = next((reg for reg, code in region_mapping.items() if code == field), None)
                    if region:
                        response_data[region] = items
        return Response(response_data, status=status.HTTP_200_OK)


class RegionListView(ListAPIView):
    queryset = Location.objects.filter(level=1)
    serializer_class = LocationSerializer


class GetChildrenLocations(APIView):
    def get(self, request, format=None):
        region_id = request.GET.get('parent_id')
        children = Location.objects.filter(parent__hydra_id=region_id).values('id', 'name', 'hydra_id')
        serializer = LocationSerializer(children, many=True)
        return Response(serializer.data)


def address_select_view(request):
    form = AddressForm()
    return render(request, 'index.html', {'form': form})


def get_children_locations(request):
    parent_id = request.GET.get('parent_id')
    print(parent_id)
    children = Location.objects.filter(parent_id=parent_id).values('id', 'name')
    print(children)
    return JsonResponse({'children': list(children)})


class Adresses(APIView):
    @csrf_exempt
    def post(self, request):
        dsn = cx_Oracle.makedsn(host='hydra.snt.kg', port='1521', service_name='hydra')

        # Establish the database connection
        dbh = cx_Oracle.connect(user='AIS_NET',
                                password='AeFae0eeleatohraelah',
                                dsn=dsn
                                )

        num_N_REGION_ID = [51385901, 51386201, 51386001, 51385801, 51385601, 51386101, 51385501]

        with dbh.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM TABLE(SR_REGIONS_PKG_S.GET_CHILDREN_REGION_LIST(51386201))
                        """)

            rows = cursor.fetchall()
            addresses = []
            for row in rows:
                id = row[0]
                visual_code = cursor.callfunc("SR_REGIONS_PKG_S.GET_VISUAL_CODE", cx_Oracle.STRING, [id])
                print(f'{id} {visual_code} {row}')
                addresses.append(str(id)+ ' , ' +visual_code)
            process_and_save_address_data(addresses)
        return Response(status=status.HTTP_200_OK)
    
        last_key = list(address.keys())[-1]
        last_value = address[last_key]
        hydra_address = last_value['hydra_id']
        exactaddress = data.get('exactAddress', 'Значение по умолчанию').get('address', 'Значение по умолчанию')
        passport1 = data.get('assets', 'Значение по умолчанию').get('passport1', 'Значение по умолчанию')
        passport2 = data.get('assets', 'Значение по умолчанию').get('passport2', 'Значение по умолчанию')
        location_screenshot = data.get('assets', 'Значение по умолчанию').get('locationScreenShot', 'Значение по умолчанию')



# async def sms_bitrix_teh(deal_id, n_customer_id):
#     b = BitrixAsync(webhook)
#     method = 'crm.timeline.comment.add'
#     params = {'fields': {
#             "COMMENT": f"Создан абонент:https://hydra.snt.kg:8000/subjects/persons/edit/{n_customer_id}"
#             "ENTITY_TYPE": 'deal',
#             'ENTITY_ID': deal_id,


#         }}
#     test = await b.call(method, params)

