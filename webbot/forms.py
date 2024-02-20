from django import forms
from .models import Location
from django.forms import ClearableFileInput, Textarea


class AddressForm(forms.Form):
    PAYMENT_CHOICES = [
        ('', 'Выберите статус'),
        ('with_payment', 'С оплатой'),
        ('without_payment', 'Без оплаты'),
    ]
    ROUTER_CHOICES = [
        ('', 'Выберите тип'),
        ('1', 'Выкуп 1500'),
        ('2', 'Выкуп 2500'),
        ('3', 'Да ВП'),
        ('4', 'Роутер абонента')
    ]
    TARIFF_CHOICES = [
        ('', 'Выберите тариф'),
        ('1', 'Sky70'),
        ('2', 'Промо70'),
        ('3', 'Промо90'),
        ('4', 'Промо100'),
        ('5', 'Оптимальный')
    ]
    TV_CHOICES = [
        ('', 'Выберите'),
        ('1', 'Приставка ВП'),
        ('2', 'Приставка выкуп'),
        ('3', 'Приложение'),
        ('4', 'Своя приставка'),
        ('5', 'Нет')
    ]
    region = forms.ModelChoiceField(queryset=Location.objects.filter(level=1), required=False, label='Локация',
                                    empty_label="Выберите регион")
    city = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                  empty_label="Выберите город")
    district = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                      empty_label="Выберите район")
    neighborhood = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                          empty_label="Выберите микрорайон")
    street = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                    empty_label="Выберите улицу")
    building = forms.ModelChoiceField(queryset=Location.objects.none(), required=False, label='',
                                      empty_label="Выберите здание")
    final_address = forms.CharField(widget=forms.TextInput(attrs={'style': 'display:none;', 'placeholder': 'Введите точный адрес'}), required=False, label='')
    payment_type = forms.ChoiceField(widget=forms.Select,choices=PAYMENT_CHOICES,label='Статус заявки')
    router = forms.ChoiceField(widget=forms.Select, choices=ROUTER_CHOICES, label='Установка Роутера')
    tariff = forms.ChoiceField(widget=forms.Select, choices=TARIFF_CHOICES, label='Тариф')
    supertv = forms.ChoiceField(widget=forms.Select, choices=TV_CHOICES, label='Установка SuperTV')
    screenshot_location = forms.ImageField(
        widget=ClearableFileInput(),
        required=False,
        label='Cкриншот локации'
    )
    screenshot_passport_front = forms.ImageField(
            widget=ClearableFileInput(),
            required=False,
            label='Лицевая сторона паспорта'
        )
    screenshot_passport_back = forms.ImageField(
        widget=ClearableFileInput(),
        required=False,
        label='Обратная сторона паспорта'
    )
    description = forms.CharField(
        widget=Textarea(attrs={'rows': 4, 'cols': 30}),
        label='Описание',
        required=False
    )