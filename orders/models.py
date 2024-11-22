from django.contrib.auth.models import User
from django.db import models
from django.db.models import TextChoices
from django.utils.html import format_html


# Create your models here.
class DesignStatus(TextChoices):
    NONE = 'none', '-----'
    MANUFACTURED = 'manufactured', 'Виготовлено'
    STOPPED = 'stopped', 'Розробка зупинена'
    IN_PROGRESS = 'in_progress', 'В розробці'


class FilesAllowedExtensions(models.Model):
    extension = models.CharField(verbose_name='Дозволений формат для завантаження на сайт', max_length=10, unique=True)
    work_file = models.BooleanField(verbose_name='робочий файл')

    def __str__(self):
        return self.extension

    class Meta:
        verbose_name = 'Дозволений формат файлів'
        verbose_name_plural = 'Дозволені формати файлів'


class RegistrationSamples(models.Model):
    name = models.CharField(verbose_name='Назва зразку', max_length=255)
    our_manager = models.ForeignKey(User, models.DO_NOTHING, verbose_name='Хто заніс у базу')
    contact = models.CharField(verbose_name='Хто передав', max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name='Фотографія', upload_to='samples/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Зразок'
        verbose_name_plural = 'Зразки'

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" />', self.image.url)
        return "Без зображення"

    image_tag.short_description = 'Фото зразка'


class PackingType(models.Model):
    type = models.CharField(verbose_name="Тип упаковки", max_length=255)

    class Meta:
        verbose_name = 'Тип упаковки'
        verbose_name_plural = 'Типи упаковок'

    def __str__(self):
        return self.type


class DesignRegister(models.Model):
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True, editable=False,
                                        verbose_name="Дата реєстрації завдання")
    name = models.CharField(verbose_name='Назва макету', max_length=255)
    company_client_id = models.IntegerField(
        verbose_name="ID клієнта",
        blank=True,
        null=True
    )
    printing_company_id = models.IntegerField(verbose_name="ID друкарської компанії", blank=True, null=True, )
    company_manager = models.CharField(verbose_name="менеджер замовника", max_length=255, blank=True, null=True,)
    manager = models.ForeignKey(
        User,
        models.DO_NOTHING,
        verbose_name='Менеджер',
        related_name='managed_designs', blank=True, null=True
    )
    designer = models.ForeignKey(
        User,
        models.DO_NOTHING,
        verbose_name='Дизайнер',
        related_name='designed_designs', blank=True, null=True
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=DesignStatus.choices,
        default=DesignStatus.NONE
    )

    sample = models.ForeignKey(RegistrationSamples, models.DO_NOTHING, verbose_name="Зразок", blank=True, null=True)
    design_folder = models.CharField(verbose_name='Де лежить макет', blank=True, null=True, max_length=255)
    old_work = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        verbose_name="Попередня робота",
        blank=True,
        null=True
    )

    have_vector = models.BooleanField(verbose_name="наявність векторних файлів від замовника", null=True, blank=True)

    printing_machine_id = models.IntegerField(verbose_name="ID друкарської машини", blank=True, null=True, )
    packing_type = models.ForeignKey(PackingType, on_delete=models.PROTECT, verbose_name="Тип упаковки", blank=True, null=True )
    packing_size = models.CharField(verbose_name="Розмір упаков", max_length=255, blank=True, null=True)

    material_thickness = models.FloatField(verbose_name="Товщина полімеру", blank=True, null=True)
    material_id = models.IntegerField(verbose_name="ID матеріалу", blank=True, null=True)
    ruling = models.IntegerField(verbose_name="лініатура растру", blank=True, null=True)

    color_count_face = models.IntegerField(verbose_name="кількість кольорів лице", blank=True, null=True)
    color_count_back = models.IntegerField(verbose_name="кількість кольорів зворот", blank=True, null=True)

    colors = models.CharField(verbose_name="Кольори", max_length=255, blank=True, null=True)

    rapport = models.FloatField(verbose_name="рапорт", blank=True, null=True)

    is_revert_print = models.BooleanField(verbose_name="Друк", blank=True, null=True)
    tracks_count = models.IntegerField(verbose_name="кількість доріжок", blank=True, null=True)

    class Meta:
        verbose_name = 'Реєстр дизайнів'
        verbose_name_plural = 'Реєстр дизайнів'

    def __str__(self):
        return f"D{self.pk} {self.name}"


class DesignTask(models.Model):
    design_order = models.ForeignKey(DesignRegister, on_delete=models.PROTECT, verbose_name="Дизайн")
    task = models.TextField(verbose_name="Завдання")
    is_complete = models.BooleanField(verbose_name="Зроблено", default=False)
    version = models.IntegerField(verbose_name="Версія", default=1)

    class Meta:
        verbose_name = 'Завдання по дизайну'
        verbose_name_plural = 'Завдання по дизайнам'

    def __str__(self):
        return f"{self.design_order} {self.task}"
