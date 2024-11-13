from django.db import models

# Create your models here.


class FilesAllowedExtensions (models.Model):
    extension = models.CharField(verbose_name='Дозволений формат для завантаження на сайт', max_length=10, unique=True)
    work_file = models.BooleanField(verbose_name='робочий файл')

    def __str__(self):
        return self.extension

    class Meta:
        verbose_name = 'Дозволений формат файлів'
        verbose_name_plural = 'Дозволені формати файлів'



