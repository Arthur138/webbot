from fast_bitrix24 import Bitrix, BitrixAsync
from django.views.decorators.csrf import csrf_exempt
from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
import json
import asyncio
import requests
import sys
from http import HTTPStatus




class Bx_neaktivka(APIView):
    def get(self, request):
        fields_list = ['UF_CRM_1669625413673', 'UF_CRM_1674993837284', 'UF_CRM_1681792838630', 'UF_CRM_1681792989530',
                       'UF_CRM_1669625771519', 'UF_CRM_1681792741017', 'UF_CRM_1673255771']
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



# async def application_zayavka():
#     webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
#     b = Bitrix(webhook)
#     method = 'crm.deal.add'
#     test = {'fields': {
#         'TITLE': 'Неактивка',  
#         'TYPE_ID': 6, 

#         'UF_CRM_1669625413673': '' ,
#         'UF_CRM_1674993837284': '' ,
#         'UF_CRM_1681792838630': '' ,
#         'UF_CRM_1681792989530': '' ,
#         'UF_CRM_1669625771519': '' , 
#         'COMMENTS': '' ,
#         'UF_CRM_1681792741017': '' , 
#         'UF_CRM_1673255771': '' ,
#         'CATEGORY_ID': '' ,
#         'ASSIGNED_BY_ID': '' ,
#         'UF_CRM_1673259335': '' ,
#         'CONTACT_ID': '' ,
#     }}
#     test2 = await b.call(method, test, raw=False)
#     print(test2)
#     return test2





