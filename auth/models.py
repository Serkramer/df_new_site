from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, unique=True)  # Use unique=True for unique email addresses
    email_token = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=255, verbose_name='Ім`я', null=True)
    last_name = models.CharField(max_length=255, verbose_name='Прізвище', null=True)
    company = models.CharField(max_length=255, verbose_name='Компанія', null=True)

    position = models.CharField(max_length=255, verbose_name='Посада', null=True)
    phone_number = models.CharField(max_length=255, verbose_name='Телефон', null=True)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False, verbose_name='Перевірена пошта')
    is_worker = models.BooleanField(default=False, verbose_name='Наш працівник')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, email=instance.email)

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профіля користувачів"
