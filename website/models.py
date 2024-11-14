from django.db import models
from django.contrib.auth.models import Group


class Menu(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='submenu')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class UserGroupMenu(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'menu')

