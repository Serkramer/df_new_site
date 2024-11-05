# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from store.models import Materials as StoreMaterial


class OrderStatusList(models.TextChoices):
    NONE = 'NONE', 'Не зазначено'
    ERROR_FILE_COUNT = 'ERROR_FILE_COUNT', 'Не вірна кількість файлів'
    CANCEL = 'CANCEL', 'Відмінено'
    STOP_BY_CLIENT = "STOP_BY_CLIENT", "Зупинене клієнтом"
    STOP = "STOP", "Зупинене"
    IN_PROCESSING = "IN_PROCESSING", "В обробці"
    WAITING_FOR_EDITS = "WAITING_FOR_EDITS", "Чекаємо правки"
    WAITING_FOR_PAYMENT = "WAITING_FOR_PAYMENT", "Чекаємо оплату"
    RIPPING = "RIPPING", "Ріпується"
    RIPPED = "RIPPED", "Відріповано"
    IN_WORK = "IN_WORK", "В роботі"
    ENGRAVED = "ENGRAVED", "Відріповано"
    PACKED = "PACKED", "Запаковано"
    SENT = "SENT", "Відправлено"
    DELIVERED = "DELIVERED", "Доставлено"


class PrintingMachineShaftsInputValueTypeList(models.TextChoices):
    DIAMETER = "DIAMETER", "Друкарський діаметр"
    RAPPORT = "RAPPORT", "Рапорт"
    METAL_DIAMETER = "METAL_DIAMETER", "Діаметр по металу"
    CIRCUMFERENCE = "CIRCUMFERENCE", "Довжина окружності"
    NUMBER_OF_TEETH = "NUMBER_OF_TEETH", "Кількість зубів"
    DISTORTION = "DISTORTION", "Компресія"


class AniloxRollTransferVolumeTypeList(models.TextChoices):
    G_PER_M2 = "G_PER_M2", "гр/м2",
    BCM = "BCM", "миллиард кубических микрон на квадратный дюйм",
    CM3_PER_M2 = "CM3_PER_M2", "см3/м2",


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('custom')


### old table, don't use
class Addressees(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_id = models.BigIntegerField(blank=True, null=True)
    contact_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addressees'


class Addresses(models.Model):
    id = models.BigAutoField(primary_key=True)
    build = models.CharField(max_length=10, blank=True, null=True)
    post_office_ref = models.CharField(max_length=36, blank=True, null=True)
    settlement_ref = models.CharField(max_length=36, blank=True, null=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    addressescol = models.CharField(max_length=45, blank=True, null=True)
    number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'

    def __str__(self):
        return f"{self.street} {self.build}"


class AdhesiveTapeThicknesses(models.Model):
    id = models.BigAutoField(primary_key=True)
    thickness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name='Товщина')

    class Meta:
        managed = False
        db_table = 'adhesive_tape_thicknesses'
        verbose_name = 'Товщина скотчу'
        verbose_name_plural = 'Товщини скотчів'

    def __str__(self):
        return f"{self.thickness}"


class AdhesiveTapes(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Опис')
    manufacturer = models.CharField(max_length=50, blank=True, null=True, verbose_name='Виробник')
    series = models.CharField(max_length=50, blank=True, null=True, verbose_name='Серія')
    thickness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True) # old
    adhesive_tape_thickness = models.ForeignKey(AdhesiveTapeThicknesses, models.DO_NOTHING, blank=True, null=True, verbose_name='товщина скотчу')

    class Meta:
        managed = False
        db_table = 'adhesive_tapes'
        verbose_name = 'Скотч'
        verbose_name_plural = 'Скотчі'

    def __str__(self):
        return (f"{self.description if self.description else ''} "
                f"{self.manufacturer  if self.manufacturer else ''} "
                f"{self. adhesive_tape_thickness if self.adhesive_tape_thickness else ''}")


# +
class AngleSetTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, blank=True, null=True, verbose_name='Назва')

    class Meta:
        managed = False
        db_table = 'angle_set_types'
        verbose_name = 'Тип набору кутів'
        verbose_name_plural = 'Типи наборів кутів'

    def __str__(self):
        return self.name


# +
class AngleSets(models.Model):
    id = models.BigAutoField(primary_key=True)
    black = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, )
    cyan = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, )
    magenta = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, )
    name = models.CharField(max_length=45, blank=True, null=True, verbose_name='Назва')
    other = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='Інші')
    yellow = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    angle_set_type = models.ForeignKey(AngleSetTypes, models.DO_NOTHING, blank=True, null=True,
                                       verbose_name='Тип набору кутів')
    green = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    orange = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    violet = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'angle_sets'
        verbose_name = 'Набір кутів'
        verbose_name_plural = 'Набіри кутів'

    def __str__(self):
        return self.name


class AniloxRolls(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Опис")
    line_count = models.IntegerField(blank=True, null=True, verbose_name='лініатура')
    transfer_volume = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="фарбоперенос")
    printing_machine = models.ForeignKey('PrintingMachines', models.DO_NOTHING, blank=True, null=True, verbose_name='Друкарська машина')
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name='вимірювання арбопереносу', choices=AniloxRollTransferVolumeTypeList.choices)

    class Meta:
        managed = False
        db_table = 'anilox_rolls'
        verbose_name = 'Анілокс'
        verbose_name_plural = 'Анілокси'

    def __str__(self):
        return f"{self.printing_machine} | {self.line_count}"


class BlackGenerations(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'black_generations'


class Branches(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_name = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branches'

    def __str__(self):
        return self.branch_name


class ClicheTechnologies(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15, blank=True, null=True, verbose_name='Назва технології')
    cliche_technology_type = models.ForeignKey('ClicheTechnologyTypes', models.DO_NOTHING, blank=True, null=True, verbose_name='Тип технології')
    len_file_resolution = models.ForeignKey('LenFileResolutions', models.DO_NOTHING, blank=True, null=True, verbose_name='Розширення')
    thickness_min = models.IntegerField(blank=True, null=True, verbose_name='Мінімальна товщина кліше для технології')
    thickness_max = models.IntegerField(blank=True, null=True, verbose_name='Максимальна товщина кліше для технології')

    class Meta:
        managed = False
        db_table = 'cliche_technologies'
        verbose_name = 'Технологія'
        verbose_name_plural = 'Технології'

    def __str__(self):
        return f"{self.name} {self.len_file_resolution}"


class ClicheTechnologiesUsesInPresets(models.Model):
    printing_machine_preset = models.OneToOneField('PrintingMachinePresets', models.DO_NOTHING,
                                                   primary_key=True)  # The composite primary key (printing_machine_preset_id, cliche_technology_id) found, that is not supported. The first column is selected.
    cliche_technology = models.ForeignKey(ClicheTechnologies, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cliche_technologies_uses_in_presets'
        unique_together = (('printing_machine_preset', 'cliche_technology'),)


class ClicheTechnologyTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    technology = models.CharField(max_length=15, blank=True, null=True, verbose_name="Назва технології")

    class Meta:
        managed = False
        db_table = 'cliche_technology_types'
        verbose_name = 'Тип технології'
        verbose_name_plural = 'Типи технологій'

    def __str__(self):
        return self.technology


class ClientUsePrintingCompany(models.Model):
    company_client = models.OneToOneField('CompanyClients', models.DO_NOTHING,
                                          primary_key=True)  # The composite primary key (company_client_id, printing_company_id) found, that is not supported. The first column is selected.
    printing_company = models.ForeignKey('PrintingCompanies', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'client_use_printing_company'
        unique_together = (('company_client', 'printing_company'),)


# +
class ColorLibraries(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Назва бібліотеки")
    type = models.CharField(max_length=25, blank=True, null=True, verbose_name="Тип")

    class Meta:
        managed = False
        db_table = 'color_libraries'
        verbose_name = 'Бібліотека кольорів'
        verbose_name_plural = 'Бібліотеки кольорів'

    def __str__(self):
        return f'{self.type} {self.description}'


class ColorProfileVersions(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_profile_versions'


class ColorProfiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    black_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING, blank=True, null=True)
    cyan_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                         related_name='colorprofiles_cyan_anilox_roll_set', blank=True, null=True)
    green_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                          related_name='colorprofiles_green_anilox_roll_set', blank=True, null=True)
    magenta_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                            related_name='colorprofiles_magenta_anilox_roll_set', blank=True,
                                            null=True)
    orange_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                           related_name='colorprofiles_orange_anilox_roll_set', blank=True, null=True)
    spot_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                         related_name='colorprofiles_spot_anilox_roll_set', blank=True, null=True)
    violet_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                           related_name='colorprofiles_violet_anilox_roll_set', blank=True, null=True)
    white_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                          related_name='colorprofiles_white_anilox_roll_set', blank=True, null=True)
    yellow_anilox_roll = models.ForeignKey(AniloxRolls, models.DO_NOTHING,
                                           related_name='colorprofiles_yellow_anilox_roll_set', blank=True, null=True)
    color_profile_file_name = models.CharField(max_length=100, blank=True, null=True)
    printing_material = models.ForeignKey('PrintingMaterials', models.DO_NOTHING, blank=True, null=True)
    date_build_profiles = models.DateTimeField(blank=True, null=True)
    date_made_forms = models.DateTimeField(blank=True, null=True)
    is_revert_printing = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    raster_dot = models.ForeignKey('RasterDots', models.DO_NOTHING, blank=True, null=True)
    ruling = models.ForeignKey('Rulings', models.DO_NOTHING, blank=True, null=True)
    printing_company = models.ForeignKey('PrintingCompanies', models.DO_NOTHING, blank=True, null=True)
    adhesive_tape = models.ForeignKey(AdhesiveTapes, models.DO_NOTHING, blank=True, null=True)
    dye = models.ForeignKey('Dyes', models.DO_NOTHING, blank=True, null=True)
    laminate_printing_material = models.ForeignKey('PrintingMaterials', models.DO_NOTHING,
                                                   related_name='colorprofiles_laminate_printing_material_set',
                                                   blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    printing_machine = models.ForeignKey('PrintingMachines', models.DO_NOTHING, blank=True, null=True)
    base_printing_material = models.ForeignKey('PrintingMaterials', models.DO_NOTHING,
                                               related_name='colorprofiles_base_printing_material_set', blank=True,
                                               null=True)
    raster_start = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    smoothing = models.IntegerField(blank=True, null=True)
    black_generation = models.ForeignKey(BlackGenerations, models.DO_NOTHING, blank=True, null=True)
    version = models.ForeignKey(ColorProfileVersions, models.DO_NOTHING, blank=True, null=True)
    parent_color_profile = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_profiles'
        verbose_name_plural = "Кольорові профіля"
        verbose_name = "Кольоровий профіль"

    def __str__(self):
        return self.color_profile_file_name


class ColorProofOrderNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    header = models.CharField(max_length=45, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    color_proof_order = models.ForeignKey('ColorProofOrders', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_proof_order_notes'
        verbose_name = 'коментар до замовлення кольоропроби'
        verbose_name_plural = 'коментарі до замовлення кольоропроби'

    def __str__(self):
        return f"{self.header if self.header else ''} {self.text if self.text else ''}"


class ColorProofOrderPaymentAmortizations(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    value = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    color_proof_order_payment = models.ForeignKey('ColorProofOrderPayments', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_proof_order_payment_amortizations'


class ColorProofOrderPaymentTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(unique=True, max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_proof_order_payment_types'


class ColorProofOrderPaymentVarieties(models.Model):
    id = models.BigAutoField(primary_key=True)
    variety = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_proof_order_payment_varieties'


class ColorProofOrderPayments(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    color_proof_order = models.ForeignKey('ColorProofOrders', models.DO_NOTHING, blank=True, null=True)
    color_proof_order_payment_type = models.ForeignKey(ColorProofOrderPaymentTypes, models.DO_NOTHING, blank=True,
                                                       null=True)
    billing_date = models.DateTimeField(blank=True, null=True)
    color_proof_order_payment_variety = models.ForeignKey(ColorProofOrderPaymentVarieties, models.DO_NOTHING,
                                                          blank=True, null=True)
    payment_account_number = models.CharField(max_length=25, blank=True, null=True)
    payment_act = models.CharField(max_length=25, blank=True, null=True)
    sales_invoice = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_proof_order_payments'


class ColorProofOrders(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_cmyk = models.BooleanField(blank=True, null=True, verbose_name='Це cmyk?', help_text="якщо вибрати ні, то мається на увазі що в макеті є тільки пантони")  # This field type is a guess.
    color_proof_file_name = models.CharField(max_length=255, blank=True, null=True) # old
    count = models.IntegerField(blank=True, null=True, verbose_name='кількість')
    height = models.IntegerField(blank=True, null=True, verbose_name="Висота")
    launch_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата запуску')
    login = models.CharField(max_length=100, blank=True, null=True)
    urgency = models.BooleanField(blank=True, null=True, verbose_name="термінова")  # This field type is a guess.
    width = models.IntegerField(blank=True, null=True, verbose_name="ширина")
    order_delivery = models.ForeignKey('OrderDeliveries', models.DO_NOTHING, blank=True, null=True, verbose_name="доставка" )
    company_client = models.ForeignKey('CompanyClients', models.DO_NOTHING, blank=True, null=True, verbose_name="Замовник")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Назва")
    paper_id = models.BigIntegerField(blank=True, null=True, verbose_name="Бумага")
    color_profile = models.ForeignKey(ColorProfiles, models.DO_NOTHING, blank=True, null=True, verbose_name="Кольоровий профіль")
    paper_size = models.ForeignKey('PaperSizes', models.DO_NOTHING, blank=True, null=True, verbose_name="Розмір паперу")
    status = models.CharField(max_length=255, blank=True, null=True, verbose_name="Статус")
    file_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Назва файлу")
    company_our_brand = models.ForeignKey('CompanyOurBrands', models.DO_NOTHING, blank=True, null=True, verbose_name="Наша компанія")

    class Meta:
        managed = False
        db_table = 'color_proof_orders'
        verbose_name = 'Кольоропроба'
        verbose_name_plural = 'Кольоропроби'

    def __str__(self):
        return f"№ {self.id}, {self.name}"


# +
class Colors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Назва')
    red = models.IntegerField(blank=True, null=True)
    green = models.IntegerField(blank=True, null=True)
    blue = models.IntegerField(blank=True, null=True)
    html = models.CharField(max_length=255, blank=True, null=True)
    color_library = models.ForeignKey(ColorLibraries, models.DO_NOTHING, blank=True, null=True,
                                      verbose_name='Бібліотека кольорів')

    class Meta:
        managed = False
        db_table = 'colors'
        verbose_name = 'Кольор'
        verbose_name_plural = 'Кольори'


class Companies(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Повне ім`я",
                                 help_text='обов`язково повинно співпадати символ в символ з 1С')
    name = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name="Ім`я")
    okpo = models.CharField(max_length=15, blank=True, null=True, verbose_name="ЄРДПО")
    delivery_preset = models.ForeignKey('DeliveryPresets', models.DO_NOTHING, blank=True, null=True,
                                        verbose_name="Доставка за умовчанням")
    company_group = models.ForeignKey('CompanyGroups', models.DO_NOTHING, blank=True, null=True,
                                      verbose_name='Група компаній')
    contact = models.ForeignKey('Contacts', models.DO_NOTHING, blank=True, null=True, verbose_name="Контакт за умовчанням")
    is_verified = models.BooleanField(blank=True, null=True, verbose_name="Перевірений")  # This field type is a guess.
    is_outdated = models.BooleanField(blank=True, null=True, verbose_name="Застарілий")  # This field type is a guess.
    number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Тел. номер юр. особи")

    class Meta:
        managed = False
        db_table = 'companies'
        verbose_name = 'Компанія'
        verbose_name_plural = 'Компанії'

    def __str__(self):
        return f"{self.name}"


class CompaniesContacts(models.Model):
    comment = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.OneToOneField(Companies, models.DO_NOTHING,
                                   primary_key=True)  # The composite primary key (company_id, contact_id) found, that is not supported. The first column is selected.
    contact = models.ForeignKey('Contacts', models.DO_NOTHING)
    is_logistic = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    percent_bonus = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companies_contacts'
        unique_together = (('company', 'contact'),)


class CompanyClients(models.Model):
    id = models.OneToOneField(Companies, models.DO_NOTHING, db_column='id', primary_key=True, verbose_name='Компанія')
    is_banned = models.BooleanField(blank=True, null=True, verbose_name='Заблокований')  # This field type is a guess.
    debt = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, verbose_name='Борг')
    company_our_brand = models.ForeignKey('CompanyOurBrands', models.DO_NOTHING, blank=True, null=True,
                                          verbose_name='З якою нашою компанією працюємо')
    document_delivery_type = models.CharField(max_length=255, blank=True, null=True,
                                              verbose_name='Доставка документів')
    is_prepayment = models.BooleanField(blank=True, null=True,
                                        verbose_name='По передплаті')  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'company_clients'
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'

    def __str__(self):
        return f"{self.id.name}"


class CompanyGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_groups'
        verbose_name = 'Група компаній'
        verbose_name_plural = 'Групи компаній'

    def __str__(self):
        return self.name


class CompanyNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    header = models.CharField(max_length=45, blank=True, null=True)
    text = models.CharField(max_length=255)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_notes'


class CompanyNotifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    actions_on_products = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)
    contacts_detail = models.ForeignKey('ContactsDetails', models.DO_NOTHING, blank=True, null=True)
    message_text = models.ForeignKey('MessageTexts', models.DO_NOTHING, blank=True, null=True)
    company_to = models.ForeignKey(Companies, models.DO_NOTHING, related_name='companynotifications_company_to_set',
                                   blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_notifications'


class CompanyOurBrands(models.Model):
    id = models.OneToOneField(Companies, models.DO_NOTHING, db_column='id', primary_key=True)
    abbreviation = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_our_brands'
        verbose_name = 'Наша компанія'
        verbose_name_plural = 'Наші компанії'

    def __str__(self):
        return self.id.name


class CompressionTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compression_types'

    def __str__(self):
        return self.type


class ContactInfoTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'contact_info_types'
        verbose_name = 'Тип контакту'
        verbose_name_plural = "Типи контактів"

    def __str__(self):
        return self.type


class ContactTypes(models.Model):
    contacts_detail = models.ForeignKey('ContactsDetails', models.DO_NOTHING)
    type = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_types'


class Contacts(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="коментар")
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Ім'я")
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Прізвище")
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="по-батькові")
    contacts_detail = models.ForeignKey('ContactsDetails', models.DO_NOTHING, blank=True, null=True,
                                        verbose_name='контакти')
    mail_contacts_detail = models.ForeignKey('ContactsDetails', models.DO_NOTHING,
                                             related_name='contacts_mail_contacts_detail_set', blank=True, null=True,
                                             verbose_name='пошти')
    phone_contacts_detail = models.ForeignKey('ContactsDetails', models.DO_NOTHING,
                                              related_name='contacts_phone_contacts_detail_set', blank=True, null=True,
                                              verbose_name='телефони')
    bonus_area = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакти'

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.description}"


class ContactsDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=75)
    contact = models.ForeignKey(Contacts, models.DO_NOTHING, blank=True, null=True)
    contact_info_type = models.ForeignKey(ContactInfoTypes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts_details'
        verbose_name = 'Контактна інформація'
        verbose_name_plural = 'контактна інформація'

    def __str__(self):
        return self.value


class Curriers(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    tel_currier = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'curriers'


class CurveListInStrategy(models.Model):
    curve_strategy = models.OneToOneField('CurveStrategies', models.DO_NOTHING,
                                          primary_key=True)  # The composite primary key (curve_strategy_id, curve_id) found, that is not supported. The first column is selected.
    curve = models.ForeignKey('Curves', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'curve_list_in_strategy'
        unique_together = (('curve_strategy', 'curve'),)


class CurveStrategies(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=150, verbose_name="назва файлу")

    class Meta:
        managed = False
        db_table = 'curve_strategies'
        verbose_name = 'curve_strategy'
        verbose_name_plural = 'curve_strategies'

    def __str__(self):
        return self.file_name


class Curves(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'curves'

    def __str__(self):
        return self.file_name


class DeliveryPresetForOurCompanies(models.Model):
    id = models.OneToOneField('DeliveryPresets', models.DO_NOTHING, db_column='id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'delivery_preset_for_our_companies'


class DeliveryPresets(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Коментар')
    name = models.CharField(max_length=100, verbose_name="Назва доставки")
    address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True, verbose_name="Адресса")
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True,  verbose_name="Компанія")
    delivery_type = models.ForeignKey('DeliveryTypes', models.DO_NOTHING, blank=True, null=True, verbose_name='Тип доставки')
    contact = models.ForeignKey(Contacts, models.DO_NOTHING, blank=True, null=True,  verbose_name="Контакт")
    is_legal_address = models.BooleanField(blank=True, null=True,  verbose_name="Перевірена адреса")  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'delivery_presets'
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"

    def __str__(self):
        delivery_str = f"{self.delivery_type} | "

        if self.address.settlement_ref:
            delivery_str += f"{self.address} "

        if self.delivery_type.id == 3 and self.address.post_office_ref:

            #TODO get_post_office_str
            # delivery_str += f"{self.address.post_office_ref} "
            delivery_str += f"{self.name} "
        else:
            delivery_str += f"{self.address} "
        return delivery_str


class DeliveryTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'delivery_types'

    def __str__(self):
        return self.type


class Dyes(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    series = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dyes'


class EmployeeRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_roles'


class Employees(models.Model):
    id = models.BigAutoField(primary_key=True)
    birthday = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    middle_name = models.CharField(max_length=45, blank=True, null=True)
    employee_role = models.ForeignKey(EmployeeRoles, models.DO_NOTHING, blank=True, null=True)
    account_name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    employee_role_0 = models.CharField(db_column='employee_role', max_length=255, blank=True,
                                       null=True)  # Field renamed because of name conflict.
    login = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'


class Engravers(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engravers'
        verbose_name_plural = 'Гравери'
        verbose_name = 'Гравер'

    def __str__(self):
        return self.full_name


class FartukHeights(models.Model):
    id = models.BigAutoField(primary_key=True)
    height = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, verbose_name='Висота')
    fartuk = models.ForeignKey('Fartuks', models.DO_NOTHING, blank=True, null=True, verbose_name='Фартук')
    printing_machine = models.ForeignKey('PrintingMachines', models.DO_NOTHING, blank=True, null=True,
                                         verbose_name="друкарська машина")

    class Meta:
        managed = False
        db_table = 'fartuk_heights'
        verbose_name = 'Висота фартука'
        verbose_name_plural = 'Висоти фартуків'

    def __str__(self):
        return f"{self.fartuk} {self.height}"


# +
class FartukMembraneTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=30, blank=True, null=True, verbose_name='Тип мембрани')
    thickness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True,
                                    verbose_name="Товщіна мембрани")

    class Meta:
        managed = False
        db_table = 'fartuk_membrane_types'
        verbose_name = 'Тип мембрани фартука'
        verbose_name_plural = 'Типи мембран фартуків'

    def __str__(self):
        return f"{self.type} {self.thickness}"


# +
class FartukRailTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип планки')

    class Meta:
        managed = False
        db_table = 'fartuk_rail_types'
        verbose_name = 'Тип планки фартука'
        verbose_name_plural = 'Типи планок для фартуків'

    def __str__(self):
        return self.type


# +
class Fartuks(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name='Опис')
    max_height = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True,
                                     verbose_name='Максимальна висота')
    max_width = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True,
                                    verbose_name='Максимальна ширина')
    type = models.CharField(max_length=15, blank=True, null=True, verbose_name='Тип фартуку')
    bottom_fartuk_rail_type = models.ForeignKey(FartukRailTypes, models.DO_NOTHING, blank=True, null=True,
                                                verbose_name='Тип нижньої планки')
    fartuk_membrane_type = models.ForeignKey(FartukMembraneTypes, models.DO_NOTHING, blank=True, null=True,
                                             verbose_name='Тип мембрани')
    top_fartuk_rail_type = models.ForeignKey(FartukRailTypes, models.DO_NOTHING,
                                             related_name='fartuks_top_fartuk_rail_type_set', blank=True, null=True,
                                             verbose_name='Тип верхньої планки')
    is_fixed = models.BooleanField(blank=True, null=True, verbose_name="Фіксований")  # This field type is a guess.
    height = models.IntegerField(blank=True, null=True, verbose_name='Висота')
    thickness = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, )

    class Meta:
        managed = False
        db_table = 'fartuks'
        verbose_name = 'Фартук'
        verbose_name_plural = 'Фартуки'

    def __str__(self):
        return self.type


# +
class LenFileResolutions(models.Model):
    id = models.BigAutoField(primary_key=True)
    resolution = models.IntegerField(blank=True, null=True, verbose_name='Роздільна здатність')

    class Meta:
        managed = False
        db_table = 'len_file_resolutions'
        verbose_name = 'Роздільна здатність len-файла'
        verbose_name_plural = 'Роздільні здатністі len-файлів'

    def __str__(self):
        return f'{self.resolution}'


class Lineatures(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.IntegerField(blank=True, null=True)
    angle_set_type = models.ForeignKey(AngleSetTypes, models.DO_NOTHING, blank=True, null=True)
    len_file_resolution = models.ForeignKey(LenFileResolutions, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lineatures'


class LogContactBonuses(models.Model):
    id = models.BigAutoField(primary_key=True)
    action = models.CharField(max_length=255)
    percent_bonus = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    contact = models.ForeignKey(Contacts, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_contact_bonuses'


class MaterialHardness(models.Model):
    id = models.BigAutoField(primary_key=True)
    hardness = models.IntegerField(blank=True, null=True)
    material_hardness_type = models.ForeignKey('MaterialHardnessTypes', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_hardness'


class MaterialHardnessTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'material_hardness_types'


class MaterialManufacturers(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_manufacturers'


class MaterialPlateTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_plate_types'


class MaterialProcessTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_process_types'


class MaterialSolvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    solvent = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_solvents'


class Materials(models.Model):
    id = models.BigAutoField(primary_key=True)
    base_thickness_max = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    base_thickness_min = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    thickness = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    material_hardness = models.ForeignKey(MaterialHardness, models.DO_NOTHING, blank=True, null=True)
    material_manufacturer = models.ForeignKey(MaterialManufacturers, models.DO_NOTHING, blank=True, null=True)
    material_plate_type = models.ForeignKey(MaterialPlateTypes, models.DO_NOTHING, blank=True, null=True)
    material_process_type = models.ForeignKey(MaterialProcessTypes, models.DO_NOTHING, blank=True, null=True)
    material_solvent = models.ForeignKey(MaterialSolvents, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materials'


class MaterialsUsesInPresets(models.Model):
    printing_machine_preset = models.OneToOneField('PrintingMachinePresets', models.DO_NOTHING,
                                                   primary_key=True)  # The composite primary key (printing_machine_preset_id, material_id) found, that is not supported. The first column is selected.
    material = models.ForeignKey(Materials, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'materials_uses_in_presets'
        unique_together = (('printing_machine_preset', 'material'),)


class MessageTexts(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.TextField(blank=True, null=True)
    header = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_texts'


class OperatorRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operator_roles'


class Operators(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    middle_name = models.CharField(max_length=45, blank=True, null=True)
    operator_role = models.ForeignKey(OperatorRoles, models.DO_NOTHING, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operators'


class OrderCompressions(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    compression_type = models.ForeignKey(CompressionTypes, models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_compressions'


class OrderDeliveries(models.Model):
    id = models.BigAutoField(primary_key=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    shipping_date_arrival = models.DateTimeField(blank=True, null=True)
    shipping_date_departure = models.DateTimeField(blank=True, null=True)
    shipping_date_planed = models.DateTimeField(blank=True, null=True)
    ttn = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)
    addressee = models.ForeignKey(Addressees, models.DO_NOTHING, blank=True, null=True)
    currier = models.ForeignKey(Curriers, models.DO_NOTHING, blank=True, null=True)
    delivery_type = models.ForeignKey(DeliveryTypes, models.DO_NOTHING, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_deliveries'


class OrderEmployee(models.Model):
    order = models.OneToOneField('Orders', models.DO_NOTHING,
                                 primary_key=True)  # The composite primary key (order_id, employee_id) found, that is not supported. The first column is selected.
    employee = models.ForeignKey(Employees, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_employee'
        unique_together = (('order', 'employee'),)


class OrderFartuks(models.Model):
    id = models.BigAutoField(primary_key=True)
    center_point = models.IntegerField(blank=True, null=True, verbose_name="центральна точка")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='коментар')
    height = models.IntegerField(blank=True, null=True, verbose_name="висота фартука")
    width = models.IntegerField(blank=True, null=True, verbose_name='ширина фартука')
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True, verbose_name='Замовленння')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Назва')

    class Meta:
        managed = False
        db_table = 'order_fartuks'
        verbose_name = "фортук в замовленні"
        verbose_name_plural = "фортуки в замовленнях"


class OrderGroups(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'order_groups'
        verbose_name = 'Група замовлень'


class OrderNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    header = models.CharField(max_length=45, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_notes'


class OrderOperator(models.Model):
    order = models.OneToOneField('Orders', models.DO_NOTHING,
                                 primary_key=True)  # The composite primary key (order_id, operator_id) found, that is not supported. The first column is selected.
    operator = models.ForeignKey(Operators, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_operator'
        unique_together = (('order', 'operator'),)


class OrderPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    order_payment_type = models.ForeignKey('OrderPaymentTypes', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_payment'


class OrderPaymentTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_payment_types'


class OrderPlaneSliceChecks(models.Model):
    id = models.BigAutoField(primary_key=True)
    angle = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    curves = models.CharField(max_length=255, blank=True, null=True)
    dot_code = models.CharField(max_length=10, blank=True, null=True)
    dot_name = models.CharField(max_length=100, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    lineature = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    resolution = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    ruling = models.ForeignKey('Rulings', models.DO_NOTHING, blank=True, null=True)
    ruling_0 = models.IntegerField(db_column='ruling', blank=True,
                                   null=True)  # Field renamed because of name conflict.
    file_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_plane_slice_checks'


class OrderPlaneSliceColorLibraries(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_plane_slice_color_libraries'


class OrderPlaneSliceColors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    red = models.IntegerField(blank=True, null=True)
    green = models.IntegerField(blank=True, null=True)
    blue = models.IntegerField(blank=True, null=True)
    html = models.CharField(max_length=7, blank=True, null=True)
    order_plane_slice_color_library = models.ForeignKey(OrderPlaneSliceColorLibraries, models.DO_NOTHING, blank=True,
                                                        null=True)

    class Meta:
        managed = False
        db_table = 'order_plane_slice_colors'


class OrderPlaneSliceFragmentChecks(models.Model):
    id = models.BigAutoField(primary_key=True)
    angle = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    dot_code = models.CharField(max_length=10, blank=True, null=True)
    dot_name = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    plate_curve = models.CharField(max_length=255, blank=True, null=True)
    press_curve = models.CharField(max_length=255, blank=True, null=True)
    ruling = models.IntegerField(blank=True, null=True)
    order_plane_slice_check = models.ForeignKey(OrderPlaneSliceChecks, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_plane_slice_fragment_checks'


class OrderPlaneSliceGroups(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'order_plane_slice_groups'


class OrderPlaneSlices(models.Model):
    id = models.BigAutoField(primary_key=True)
    height = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    lineature = models.ForeignKey(Lineatures, models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    order_plane_slice_color = models.ForeignKey(OrderPlaneSliceColors, models.DO_NOTHING, blank=True, null=True)
    raster_dot = models.ForeignKey('RasterDots', models.DO_NOTHING, blank=True, null=True)
    angle = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    material_plate_type = models.ForeignKey(MaterialPlateTypes, models.DO_NOTHING, blank=True, null=True)
    order_plane_slice_group = models.ForeignKey(OrderPlaneSliceGroups, models.DO_NOTHING, blank=True, null=True)
    fragment_id = models.IntegerField(blank=True, null=True)
    printing_method = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Materials, models.DO_NOTHING, blank=True, null=True)
    html = models.CharField(max_length=10, blank=True, null=True)
    ruling = models.ForeignKey('Rulings', models.DO_NOTHING, blank=True, null=True)
    order_fartuk_name = models.CharField(max_length=100, blank=True, null=True)
    position_x = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    position_y = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    is_defect = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    cutting_length = models.IntegerField(blank=True, null=True)
    cutting_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_plane_slices'
        verbose_name = 'форми в замовленні'


# устаревшая
class OrderStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_status'


class OrderStatusHistories(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    login = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_status_histories'


class Orders(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_defective = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    is_docs_printed = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    fartuks_area = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    forms_area = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    forms_quantity = models.IntegerField(blank=True, null=True)
    launch_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    payment_info = models.CharField(max_length=100, blank=True, null=True)
    is_revert_printing = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    urgency = models.BooleanField(blank=True, null=True, verbose_name='Термінове')  # This field type is a guess.
    angle_set = models.ForeignKey(AngleSets, models.DO_NOTHING, blank=True, null=True)
    cliche_technology = models.ForeignKey(ClicheTechnologies, models.DO_NOTHING, blank=True, null=True)
    fartuk = models.ForeignKey(Fartuks, models.DO_NOTHING, blank=True, null=True)
    material_id = models.BigIntegerField(blank=True, null=True)
    parent_order = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    order_compression = models.ForeignKey(OrderCompressions, models.DO_NOTHING, blank=True, null=True)
    order_delivery = models.ForeignKey(OrderDeliveries, models.DO_NOTHING, blank=True, null=True)
    company_client = models.ForeignKey(CompanyClients, models.DO_NOTHING, blank=True, null=True)
    printing_company = models.ForeignKey('PrintingCompanies', models.DO_NOTHING, blank=True, null=True)
    printing_machine = models.ForeignKey('PrintingMachines', models.DO_NOTHING, blank=True, null=True)
    yellow_ruling = models.ForeignKey('YellowRulings', models.DO_NOTHING, blank=True, null=True)
    order_group = models.ForeignKey(OrderGroups, models.DO_NOTHING, blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=255, choices=OrderStatusList.choices)
    xml_file = models.TextField(blank=True, null=True)
    plate_curve_strategy = models.ForeignKey(CurveStrategies, models.DO_NOTHING, blank=True, null=True)
    press_curve_strategy = models.ForeignKey(CurveStrategies, models.DO_NOTHING,
                                             related_name='orders_press_curve_strategy_set', blank=True, null=True)
    work_file_name = models.CharField(max_length=255, blank=True, null=True)
    is_xml_exist = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    printing_machine_preset = models.ForeignKey('PrintingMachinePresets', models.DO_NOTHING, blank=True, null=True)
    xml_status = models.CharField(max_length=255, blank=True, null=True)
    log_id = models.IntegerField(blank=True, null=True)
    branch = models.ForeignKey(Branches, models.DO_NOTHING, blank=True, null=True, verbose_name='Філіал')
    overprint_black = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    forms_area_append = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    engraver = models.ForeignKey(Engravers, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return f'{self.id} {self.company_client} {self.name}'

    def get_order_material_name(self):
        if self.material_id:
            material = StoreMaterial.objects.using('store').get(id=self.material_id)
            if material.name:
                return material.name
            else:
                return "У матеріала немає назви"
        return "-----"


class PaddingForMaterial(models.Model):
    material_id = models.BigIntegerField(primary_key=True)
    padding_bottom = models.IntegerField(blank=True, null=True)
    padding_left = models.IntegerField(blank=True, null=True)
    padding_right = models.IntegerField(blank=True, null=True)
    padding_top = models.IntegerField(blank=True, null=True)
    printing_company = models.ForeignKey('PrintingCompanies', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'padding_for_material'
        unique_together = (('material_id', 'printing_company'),)


# +
class PaperSizes(models.Model):
    id = models.BigAutoField(primary_key=True)
    height = models.IntegerField(blank=True, null=True, verbose_name='Висота')
    width = models.IntegerField(blank=True, null=True, verbose_name='Ширина')
    type = models.CharField(max_length=15, blank=True, null=True, verbose_name='Тип паперу')
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Ціна')

    class Meta:
        managed = False
        db_table = 'paper_sizes'
        verbose_name = 'Розмір папіру'
        verbose_name_plural = 'Розміри паперу'

    def __str__(self):
        return f"{self.type} {self.height}x{self.width} Ціна: {self.cost} за шт."


class PrintingCompanies(models.Model):
    id = models.OneToOneField(Companies, models.DO_NOTHING, db_column='id', primary_key=True, verbose_name='Компанія')
    process_id = models.CharField(max_length=45, blank=True, null=True, verbose_name='ID в заявці')
    color_library = models.ForeignKey(ColorLibraries, models.DO_NOTHING, blank=True, null=True,
                                      verbose_name='Бібліотека кольорів')
    need_printout = models.BooleanField(blank=True, null=True,
                                        verbose_name='Чи потрібны документи')  # This field type is a guess.
    use_low_base = models.BooleanField(blank=True, null=True,
                                       verbose_name='Використовує занижений цоколь')  # This field type is a guess.
    need_label = models.BooleanField(blank=True, null=True,
                                     verbose_name="Чи потрібен підпис")  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'printing_companies'
        verbose_name = 'Друкарська компанія'
        verbose_name_plural = 'Друкарські компанії'

    def __str__(self):
        return self.id.name


class PrintingMachinePresets(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile_file_name = models.CharField(max_length=75, blank=True, null=True,)
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Назва пресету')
    angle_set = models.ForeignKey(AngleSets, models.DO_NOTHING, blank=True, null=True, verbose_name='Набір кутів')
    lineature = models.ForeignKey(Lineatures, models.DO_NOTHING, blank=True, null=True, )
    printing_machine = models.ForeignKey('PrintingMachines', models.DO_NOTHING, blank=True, null=True, verbose_name='друкарські машини')
    raster_dot = models.ForeignKey('RasterDots', models.DO_NOTHING, blank=True, null=True, verbose_name='растрова точка')
    cliche_technology = models.ForeignKey(ClicheTechnologies, models.DO_NOTHING, blank=True, null=True, verbose_name='технологія')
    is_revert_printing = models.BooleanField(blank=True, null=True, verbose_name='зворотній друк', help_text='якщо зворотный треба вибрати так, якщо прямий - ні')  # This field type is a guess.
    color_profile = models.ForeignKey(ColorProfiles, models.DO_NOTHING, blank=True, null=True, verbose_name='профіль')
    curve_strategy = models.ForeignKey(CurveStrategies, models.DO_NOTHING, blank=True, null=True,)
    material = models.ForeignKey(Materials, models.DO_NOTHING, blank=True, null=True, verbose_name='Матеріал ?????')
    plate_curve_strategy = models.ForeignKey(CurveStrategies, models.DO_NOTHING,
                                             related_name='printingmachinepresets_plate_curve_strategy_set',
                                             blank=True,
                                             null=True,
                                             verbose_name='plate_curve_strategy')
    press_curve_strategy = models.ForeignKey(CurveStrategies, models.DO_NOTHING,
                                             related_name='printingmachinepresets_press_curve_strategy_set',
                                             blank=True,
                                             null=True,
                                             verbose_name='press_curve_strategy')
    ruling = models.ForeignKey('Rulings', models.DO_NOTHING, blank=True, null=True, verbose_name='лініатури')
    damper = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='товщина демферу, мм')
    scotch = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="коментар")
    material_thickness = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='Товщина матеріалу')
    adhesive_tape_thickness_multiplier = models.IntegerField(blank=True, null=True, verbose_name="кількість шарів скотчу" )
    adhesive_tape_thickness = models.ForeignKey(AdhesiveTapeThicknesses, models.DO_NOTHING, blank=True, null=True, verbose_name="Товщина скотчу")
    fartuk = models.ForeignKey(Fartuks, models.DO_NOTHING, blank=True, null=True, verbose_name='фартук')

    class Meta:
        managed = False
        db_table = 'printing_machine_presets'
        verbose_name = 'Пресет друкарської машини'
        verbose_name_plural = 'Пресети друкарських машин'

    def __str__(self):
        return f"{self.printing_machine} {self.name}, лініатура {self.ruling}, матеріал {self.material_thickness} "


class PrintingMachineShafts(models.Model):
    id = models.BigAutoField(primary_key=True)
    diameter = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='діаметр')
    quantity = models.IntegerField(blank=True, null=True, verbose_name='кількість')
    width = models.IntegerField(blank=True, null=True, verbose_name='ширина валу')
    printing_machine = models.ForeignKey('PrintingMachines', models.DO_NOTHING, blank=True, null=True,
                                         verbose_name='Друкарська машина')
    thickness = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name='Товшина кліше')
    date_create = models.DateTimeField(blank=True, null=True, verbose_name='Дата створення')
    input_value = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                      verbose_name='значення заміру')
    input_value_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип заміру',
                                        choices=PrintingMachineShaftsInputValueTypeList.choices)
    contact = models.ForeignKey(Contacts, models.DO_NOTHING, blank=True, null=True, verbose_name='контакт')
    printing_width = models.IntegerField(blank=True, null=True, verbose_name='ширина друку валу')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Коментар')

    class Meta:
        managed = False
        db_table = 'printing_machine_shafts'
        verbose_name = 'Вал'
        verbose_name_plural = 'Вали'

    def __str__(self):
        return f"{self.printing_machine.name} | {self.diameter}"


class PrintingMachineShaftsUseAdhesiveTapes(models.Model):
    printing_machine_shaft = models.OneToOneField(PrintingMachineShafts, models.DO_NOTHING,
                                                  primary_key=True)  # The composite primary key (printing_machine_shaft_id, adhesive_tape_id) found, that is not supported. The first column is selected.
    adhesive_tape = models.ForeignKey(AdhesiveTapes, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'printing_machine_shafts_use_adhesive_tapes'
        unique_together = (('printing_machine_shaft', 'adhesive_tape'),)


class PrintingMachines(models.Model):
    id = models.BigAutoField(primary_key=True)
    material_thickness = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,
                                             verbose_name='Товщіна матеріалу')
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Назва')
    fartuk = models.ForeignKey(Fartuks, models.DO_NOTHING, blank=True, null=True, verbose_name='Фартук')
    printing_company = models.ForeignKey(PrintingCompanies, models.DO_NOTHING, blank=True, null=True,
                                         verbose_name='Друкарська компанія')
    section = models.IntegerField(blank=True, null=True, verbose_name='Кількість секцій')
    module = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True, verbose_name='модуль')

    class Meta:
        managed = False
        db_table = 'printing_machines'
        verbose_name = 'Друкарська машина'
        verbose_name_plural = 'Друкарські машини'

    def __str__(self):
        return f"{self.printing_company} | {self.name}"


class PrintingMaterialColors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'printing_material_colors'
        verbose_name = 'колір задруковного матеріалу'

    def __str__(self):
        return self.name


class PrintingMaterialTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'printing_material_types'
        verbose_name = 'Тип задруковуємого матеріалу'

    def __str__(self):
        return self.type


class PrintingMaterials(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    printing_material_color = models.ForeignKey(PrintingMaterialColors, models.DO_NOTHING, blank=True, null=True)
    printing_material_type = models.ForeignKey(PrintingMaterialTypes, models.DO_NOTHING, blank=True, null=True)
    is_matte = models.BooleanField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'printing_materials'


class RasterDotClicheTechnologyLimit(models.Model):
    raster_dot_list = models.OneToOneField('RasterDots', models.DO_NOTHING,
                                           primary_key=True)  # The composite primary key (raster_dot_list_id, cliche_technology_limits_id) found, that is not supported. The first column is selected.
    cliche_technology_limits = models.ForeignKey(ClicheTechnologies, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'raster_dot_cliche_technology_limit'
        unique_together = (('raster_dot_list', 'cliche_technology_limits'),)


class RasterDotLineatureLimit(models.Model):
    raster_dot_entity = models.OneToOneField('RasterDots', models.DO_NOTHING,
                                             primary_key=True)  # The composite primary key (raster_dot_entity_id, lineatures_id) found, that is not supported. The first column is selected.
    lineatures = models.ForeignKey(Lineatures, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'raster_dot_lineature_limit'
        unique_together = (('raster_dot_entity', 'lineatures'),)


# +
class RasterDotMicroscreenMainDots(models.Model):
    id = models.BigAutoField(primary_key=True)
    dot = models.CharField(max_length=45, blank=True, null=True, verbose_name="Форма точки")

    class Meta:
        managed = False
        db_table = 'raster_dot_microscreen_main_dots'
        verbose_name = 'Форма точки'
        verbose_name_plural = 'Форми точок'

    def __str__(self):
        return self.dot


# +
class RasterDotMicroscreens(models.Model):
    id = models.BigAutoField(primary_key=True)
    microscreen = models.CharField(max_length=45, blank=True, null=True, verbose_name='Мікрорастрування')

    class Meta:
        managed = False
        db_table = 'raster_dot_microscreens'
        verbose_name = 'Мікрорастрування'
        verbose_name_plural = 'Мікрорастрування'

    def __str__(self):
        return self.microscreen


# +
class RasterDotTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=45, blank=True, null=True, verbose_name='Тип мікрорастру')

    class Meta:
        managed = False
        db_table = 'raster_dot_types'
        verbose_name = 'Тип мікрорастру'
        verbose_name_plural = 'Типи мікрорастру'

    def __str__(self):
        return self.type


# +
class RasterDots(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Код растру')
    min_dot_size = models.IntegerField(blank=True, null=True, verbose_name='Мінімальний розмір точки')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Назва')
    raster_dot_microscreen = models.ForeignKey(RasterDotMicroscreens, models.DO_NOTHING, blank=True, null=True,
                                               verbose_name='Мікрорастрування')
    raster_dot_microscreen_main_dot = models.ForeignKey(RasterDotMicroscreenMainDots, models.DO_NOTHING, blank=True,
                                                        null=True, verbose_name='Форма точки')
    raster_dot_type = models.ForeignKey(RasterDotTypes, models.DO_NOTHING, blank=True, null=True,
                                        verbose_name='Тип мікрорастру')

    class Meta:
        managed = False
        db_table = 'raster_dots'
        verbose_name = 'Растрова точка'
        verbose_name_plural = 'Растрові точки'

    def __str__(self):
        return f"{self.code} {self.name}"


class RasterDotsUsesInPresets(models.Model):
    printing_machine_preset = models.OneToOneField(PrintingMachinePresets, models.DO_NOTHING,
                                                   primary_key=True, verbose_name='пресет друкарської машини')  # The composite primary key (printing_machine_preset_id, raster_dot_id) found, that is not supported. The first column is selected.
    raster_dot = models.ForeignKey(RasterDots, models.DO_NOTHING, verbose_name="растрова точка")

    class Meta:
        managed = False
        db_table = 'raster_dots_uses_in_presets'
        unique_together = (('printing_machine_preset', 'raster_dot'),)


# +
class RulingRelationships(models.Model):
    angle_set_type = models.OneToOneField(AngleSetTypes, models.DO_NOTHING,
                                          primary_key=True,
                                          verbose_name='Тип кутів')  # The composite primary key (angle_set_type_id, len_file_resolution_id, ruling_id, raster_dot_id) found, that is not supported. The first column is selected.
    len_file_resolution = models.ForeignKey(LenFileResolutions, models.DO_NOTHING,
                                            verbose_name="Роздільна здатність len-файла")
    ruling = models.ForeignKey('Rulings', models.DO_NOTHING, verbose_name="Лініатура")
    raster_dot = models.ForeignKey(RasterDots, models.DO_NOTHING, verbose_name="Растрова точка")

    class Meta:
        managed = False
        db_table = 'ruling_relationships'
        unique_together = (('angle_set_type', 'len_file_resolution', 'ruling', 'raster_dot'),)
        verbose_name = 'Зв`язок допустимих значень лініатур'
        verbose_name_plural = 'Зв`язки допустимих значень лініатур'


# +
class Rulings(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='Лініатура')

    class Meta:
        managed = False
        db_table = 'rulings'
        verbose_name = 'Лініатура'
        verbose_name_plural = 'Лініатури'

    def __str__(self):
        return f"{self.id}"


class RulingsUsesInPresets(models.Model):
    printing_machine_preset = models.OneToOneField(PrintingMachinePresets, models.DO_NOTHING,
                                                   primary_key=True)  # The composite primary key (printing_machine_preset_id, ruling_id) found, that is not supported. The first column is selected.
    ruling = models.ForeignKey(Rulings, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rulings_uses_in_presets'
        unique_together = (('printing_machine_preset', 'ruling'),)


# +
class YellowRulings(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.IntegerField(blank=True, null=True, verbose_name='Лініатура жовтого')

    class Meta:
        managed = False
        db_table = 'yellow_rulings'
        verbose_name = 'Лініатура жовтого'
        verbose_name_plural = 'Лініатури жовтого'

    def __str__(self):
        if self.value and self.value >= 0:
            return f"+{self.value} %"
        else:
            return f"{self.value} %"
