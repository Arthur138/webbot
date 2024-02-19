import cx_Oracle
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response
from webbot.utils import process_and_save_address_data
from django.http import JsonResponse
from .forms import AddressForm
from .models import Location

def address_select_view(request):
    form = AddressForm()
    return render(request, 'index.html', {'form': form})

def get_children_locations(request):
    parent_id = request.GET.get('parent_id')
    children = Location.objects.filter(parent_id=parent_id).values('id', 'name')
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
                # print((visual_code+str(id)))
            process_and_save_address_data(addresses)

        # Откройте файл на запись ('w' означает write-режим, 'encoding='utf-8' гарантирует поддержку кириллицы и других символов)

            # Запись каждого адреса в файл с новой строки
            # for address in addresses:


        # print(f"Данные успешно записаны в файл {file_path}")
        # address= ['51385501 Кыргызстан, Чуйская обл.',
        #     '51386301 Кыргызстан, Чуйская обл., г. Бишкек',
        #     '51445701 Кыргызстан, Чуйская обл., Ысык-Атинский р-н',
        #     '51445901 Кыргызстан, Чуйская обл., Сокулукский р-н',
        #     '9726284301 Кыргызстан, Чуйская обл., г. Бишкек, ж/м. Ак-Ордо 3',
        #     '9771086801 Кыргызстан, Чуйская обл., г. Бишкек, ж/м. Ала-Тоо 3',
        #     '9780843101 Кыргызстан, Чуйская обл., г. Бишкек, ж/м. Телевышка']

        return Response(status=status.HTTP_200_OK)