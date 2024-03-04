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

class Zayavka(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        return Response({"message": "Данные получены"}, status=200)


class bx(APIView):
    def get(self, request):
        fields_list = ['UF_CRM_1675072231', 'UF_CRM_1675071171', 'UF_CRM_1675070693', 'UF_CRM_1675071012', 'UF_CRM_1675070436' , 'UF_CRM_1675071353']
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