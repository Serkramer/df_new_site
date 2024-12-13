from django.db import models

from custom.models import Companies
from store.models import Materials


# Create your models here.

class PriceType(models.TextChoices):
    PRICE_FARTUC = 'PRICE_FARTUC', "фартука"
    PRICE_DEMPHER = 'PRICE_DEMPHER', "демфера"
    PRICE_MATERIAL = 'PRICE_MATERIAL', "матеріала"


class Price(models.Model):
    company_id = models.IntegerField(verbose_name="ID компании")  # Хранение ID компании вручную
    price = models.FloatField(verbose_name="Ціна в євро")
    thickness_list = models.JSONField(verbose_name="Товщини", default=list, null=True, blank=True)
    material_ids = models.JSONField(verbose_name="ID материалов", default=list, blank=True)
    price_type = models.CharField(verbose_name='Ціна для', choices=PriceType.choices, default=PriceType.PRICE_MATERIAL,
                                  max_length=14)

    def get_company(self):
        # Получаем объект компании из базы custom

        return Companies.objects.using('custom').get(id=self.company_id)

    def get_materials(self):
        # Получаем объекты материалов из базы store
        return Materials.objects.using('store').filter(id__in=self.material_ids)

    def __str__(self):
        company = Companies.objects.using('custom').get(id=self.company_id)
        return f"{company} {self.price}"

    class Meta:
        verbose_name = 'Ціна'
        verbose_name_plural = 'Ціни'


class CompanyWithNuances(models.Model):
    company_id = models.IntegerField(verbose_name="ID компаниї", primary_key=True, auto_created=False, unique=True)
    check_with_cents = models.BooleanField(verbose_name="Разунок з копійками", default=False)
    name_order_in_check = models.BooleanField(verbose_name="Назва замовлення в рахунку", default=True)
    group_orders = models.BooleanField(verbose_name="Групувати замовлення в один рахунок", default=False)
    text_before = models.CharField(verbose_name="Текст перед назвою роботи", max_length=255, null=True, blank=True,
                                   default="Кліше")
    unique_order_name = models.BooleanField(verbose_name="Є нюанси в назві замовлення", default=False)
    add_prepress_in_square = models.BooleanField(verbose_name="Додавати додруківку у площу", default=True)


    def get_company(self):
        return Companies.objects.using('custom').get(id=self.company_id)

    def __str__(self):
        company = Companies.objects.using('custom').get(id=self.company_id)
        return f"{company}"

    class Meta:
        verbose_name = "Компанія, для якої є нюанси в рахунках"
        verbose_name_plural = "Компанія, для яких є нюанси в рахунках"


class Check(models.Model):
    one_c_number = models.IntegerField(verbose_name="Номер рахунку в 1С")
    client_company_id = models.IntegerField(verbose_name="ID компаниї замовника")
    order_list = models.JSONField(verbose_name="Список замовлень", default=list)
    exchange = models.FloatField(verbose_name="Курс євро")
    check_price = models.FloatField(verbose_name="Вартість кліше")
    prepress = models.FloatField(verbose_name="Додруківська підготовка")

    class Meta:
        verbose_name = "Рахунок"
        verbose_name_plural = "Рахунки"


class OrdersInCheck(models.Model):
    pass

