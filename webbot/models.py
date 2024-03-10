from django.db import models
import asyncio
from fast_bitrix24 import Bitrix
from django.contrib.auth import get_user_model



class Location(models.Model):
    hydra_id = models.IntegerField()
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    level = models.IntegerField()

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f'{self.name}'


class Supervizor(models.Model):
    REGION_CHOICES = (
        ('Чуйская', 'Чуйская'),
        ('Иссык-кульская', 'Иссык-кульская'),
        ('Нарынская', 'Нарынская'),
        ('Джалал-Абадская', 'Джалал-Абадская'),
        ('Баткенская', 'Баткенская'),
        ('Ошская', 'Ошская'),
        ('Таласская', 'Таласская')
    )
    user = models.ForeignKey(get_user_model(), related_name='supervizor', on_delete=models.CASCADE, verbose_name='Супервайзер')
    region = models.CharField(max_length=50, choices=REGION_CHOICES, verbose_name = 'Область')
    supervizer_hydra_id = models.BigIntegerField(verbose_name='Супервайзер_ID')
    supervizer_surname = models.CharField(max_length=100,  verbose_name='ФИО супервайзера')

    def __str__(self) -> str:
        return f'{self.id} {self.supervizer_surname} {self.supervizer_hydra_id}'

    class Meta:
         verbose_name = 'Супервайзеры'
         verbose_name_plural = 'Супервайзеры'

class Agent(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='agent', on_delete=models.CASCADE, verbose_name='Агент')
    bx_id = models.CharField(null=True,blank=True,max_length=100)
    region = models.CharField(max_length=100, blank=True,null=True, verbose_name = 'Область')
    supervizer_name = models.CharField(max_length=55, null=True, blank=True)
    surname = models.CharField(max_length=50, verbose_name = 'ФИО агента')
    supervizer = models.ForeignKey(Supervizor, on_delete=models.CASCADE, related_name='super_id')
    hydra_id_sales = models.CharField(max_length=50,null=True, blank=True, verbose_name=('Гидра_ID'))

    def __str__(self) -> str:
        return f'{self.id} {self.surname}'

    def save(self, *args, **kwargs):
        region_agent = self.supervizer.region
        self.region = region_agent
        superv = self.supervizer.supervizer_surname
        self.supervizer_name = superv
        name = self.surname

        # async def main():
        #     if not self.bx_id:
        #          webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
        #          b = Bitrix(webhook)
        #          method = 'crm.deal.userfield.update'
        #          params = {
        #              "id": 1283,
        #              'fields': {
        #                  "LIST": [{"VALUE": f'{name}'}]
        #
        #              }}
        #
        #          test = await b.call(method, params)
        #     else:
        #         webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
        #         b = Bitrix(webhook)
        #         method = 'crm.deal.userfield.update'
        #         params = {
        #             "id": 1283,
        #             'fields': {
        #                 "LIST": [{"ID": f'{self.bx_id}'},
        #                     {"VALUE": f'{name}'}]
        #
        #             }}
        #
        #         test = await b.call(method, params)
        #         return test
        # asyncio.run(main())

        # async def main2():
        #     webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
        #     b = Bitrix(webhook)
        #     method = 'crm.deal.userfield.get'
        #     params = {
        #         "id": 1283}
        #
        #     test = await b.call(method, params)
        #
        #     test2 = test['LIST']
        #     for i in test2:
        #
        #         if i['VALUE']==name:
        #
        #             self.bx_id = i['ID']
        # asyncio.run(main2())
        return super().save(*args, **kwargs)

    class Meta:
         verbose_name = 'Агенты'
         verbose_name_plural = 'Агенты'
