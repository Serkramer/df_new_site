from django.db.models.signals import post_delete, pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from custom.models import ContactsDetails, Contacts, CompanyNotifications


@receiver(pre_delete, sender=ContactsDetails)
def delete_related_contacttypes(sender, instance, **kwargs):
    # Удаляем связанные записи в ContactTypes
    Contacts.objects.filter(contacts_detail=instance).update(contacts_detail=None)
    Contacts.objects.filter(mail_contacts_detail=instance).update(mail_contacts_detail=None)
    Contacts.objects.filter(phone_contacts_detail=instance).update(phone_contacts_detail=None)
    Contacts.objects.filter(phone_contacts_detail=instance).update(phone_contacts_detail=None)
    CompanyNotifications.objects.filter(contacts_detail=instance).delete()
    instance.contacttypes_set.all().delete()


@receiver(pre_save, sender=ContactsDetails)
def save_contacts_details(sender, instance, **kwargs):
    if ContactsDetails.objects.filter(contact=instance.contact, value=instance.value).exists():
        instance.pk = None
