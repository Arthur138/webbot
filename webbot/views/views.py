from fast_bitrix24 import Bitrix
import cx_Oracle
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
import requests
import asyncio
from telegraph import Telegraph
from rest_framework.parsers import MultiPartParser, FormParser



class Zayavka(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        print('---------')
        bx_region = data.get('region2', 'Значение по умолчанию')
        bx_district = data.get('district2', 'Значение по умолчанию').get('ID', 'Значение по умолчанию')
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
        
        asyncio.run(application_internet(
            bx_region, bx_district, bx_order_status, bx_router, bx_tariff, bx_tv, 
            bx_provider_from, description, username, userSirName, userPhoneNumber, 
            userAdditionalPhoneNumber, address
        ))

        async def application_internet(bx_region, bx_district, bx_order_status, bx_router, bx_tariff, bx_tv, 
                                        bx_provider_from, description, username, userSirName, userPhoneNumber, 
                                        userAdditionalPhoneNumber, address):
            webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
            b = Bitrix(webhook)  # Предполагается, что вы импортировали Bitrix из вашего модуля
            method = 'crm.deal.add'
            test = {'fields':{
                'TITLE': 'Заявка на интернет',
                'TYPE_ID':6667,
                'UF_CRM_1674993837284': address,
                'UF_CRM_1673408541': username,
                'UF_CRM_1673408700': userSirName,
                'UF_CRM_1673408725': userPhoneNumber,
                'UF_CRM_1669625413673': bx_region,
                'UF_CRM_1673255771': userAdditionalPhoneNumber,
                'UF_CRM_1673258743852': description,
                'UF_CRM_1669634833014': bx_router,
                'UF_CRM_1669625771519': bx_tariff,
                'UF_CRM_1669625805213': bx_tv,
                'UF_CRM_1673251826': bx_order_status,
                'UF_CRM_1673251960': bx_provider_from,
                'UF_CRM_1695971054382': bx_district,
                'CATEGORY_ID': 33
            }}
            test2 = await b.call(method, test, raw=False)
            return test2
        return Response({"message": "Данные получены"}, status=200)

class Bx_router(APIView):
    def get(self, request):
        fields_list = ['UF_CRM_1669625771519', 'UF_CRM_1669634833014', 'UF_CRM_1673251826', 'UF_CRM_1673251960', 'UF_CRM_1669625805213','UF_CRM_1669625805213']
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
        fields_list = ['UF_CRM_1675072231', 'UF_CRM_1675071171', 'UF_CRM_1675070693', 'UF_CRM_1675071012', 'UF_CRM_1675070436' ]
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
                FROM TABLE(SR_REGIONS_PKG_S.GET_CHILDREN_REGION_LIST(51385501))
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
    




# async def sms_bitrix_teh(deal_id, n_customer_id):
#     b = BitrixAsync(webhook)
#     method = 'crm.timeline.comment.add'
#     params = {'fields': {
#             "COMMENT": f"Создан абонент:https://hydra.snt.kg:8000/subjects/persons/edit/{n_customer_id}"
#             "ENTITY_TYPE": 'deal',
#             'ENTITY_ID': deal_id,


#         }}
#     test = await b.call(method, params)

