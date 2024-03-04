import json
import asyncio
import requests
import time
from datetime import datetime
from venv import logger
import sys
from http import HTTPStatus
from urllib import parse as urllib_parse
import cx_Oracle



def create_ls_hydra():
    # print(bitrix_deal_id)
    # a = asyncio.run(bitrix_cont_ls(bitrix_deal_id))
    # contact_id = a['CONTACT_ID']
    # b = Core_to_hydra(tg_id=tg_id, bitrix_deal_id=bitrix_deal_id)
    # b.save()
    # hydra = Tg_Core.objects.get(bitrix_deal_id=bitrix_deal_id)
    # print("hydra")
    firstname = 'Arthus'
    surname = 'Test_User'
    region_id = 51385501
    tel1 = 779339944
    tel2 = 779339955
    address_id = 9984977501

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
                "vc_first_name": f"{firstname}",
                "vc_surname": f"{surname}",
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

        if region_id == 51385501:
            n_reseller_id = 7992244901
        elif region_id == 51386001:
            n_reseller_id = 7992055601
        elif region_id == 51385801:
            n_reseller_id = 7992052401
        elif region_id == 51386201:
            n_reseller_id = 7992041401
        elif region_id == 51385601:
            n_reseller_id = 7991945001
        elif region_id == 51386101:
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
                        }
                    }

                )
                print(response.status_code)

                if response.status_code == 200:
                    search_results = json.loads(response.content)
                    print("dogovor")
                    print(search_results)
                    link = f'https://hydra.snt.kg:8000/subjects/persons/edit/{n_person_id}'
                    organizations_url = urllib_parse.urljoin(hoper_url, f"subjects/customers/{n_subject_id}/contracts")
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
                        # a = hydra.ticket_tel

                        # b = hydra.ticket_tel2

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
                                    'vc_code': f"{tel2}",
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
                                        'vc_code': f"{tel1}",
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
                                time.sleep(1)

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
                                                   par_region_id=64921391,
                                                   vc_code=None,
                                                   vc_name=None,
                                                   vc_eng_name=None,
                                                   hierarchy_type_id=1037,
                                                   base_region_id=None,
                                                   par_bind_region_id=None,
                                                   realty_good_id=None,
                                                   vc_zip=None,
                                                   vc_home='Артур дом 2',
                                                   vc_building=None,
                                                   vc_construct=None,
                                                   vc_ownership=None,
                                                   vc_code_ext=None,
                                                   update_search_index=None
                                                   )

                                    dbh.commit()
                                    region_id_value = int(v_region_id.getvalue())
                                    print(f"Создана улица с ID: {region_id_value}")

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
                                            "n_region_id": 9996464001,
                                            "vc_rem": "Необходимо  уточнить",
                                            "n_addr_state_id": 1029
                                        }
                                    }

                                )

                                print(response.status_code)
                                if response.status_code == 201:
                                    search_results = json.loads(response.content)
                                    print(search_results)
# create_ls_hydra()

        #                             now = datetime.now()
        #                             test = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")
        #                             organizations_url = urllib_parse.urljoin(hoper_url,
        #                                                                      f"subjects/customers/{n_subject_id}/comments/")
        #                             asyncio.run(contact_ls(n_subject_id, hydra_ls, contact_id, adress_abon))
        #                             response = http_session.post(
        #                                 organizations_url,
        #                                 timeout=http_timeout,
        #                                 json=
        #                                 {
        #
        #                                     "comment": {
        #                                         "n_comment_type_id": 2082,
        #                                         'd_oper': f'{test}',
        #                                         "cl_comment": f" Ссылка на заявку: http://bitrix24.snt.kg/crm/deal/details/{hydra.bitrix_deal_id}/        UR ls - {lsdom}",
        #
        #                                         "n_author_id": 3778825901
        #                                     }
        #                                 }
        #
        #                             )