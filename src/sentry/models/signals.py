from __future__ import absolute_import

from django.db.models.signals import post_save
from django.dispatch import receiver

from sentry.models import Group


@receiver(post_save, sender=Group)
def resource_changed(sender, instance, created, **kwargs):
    from sentry.tasks.servicehooks import process_resource_change
    process_resource_change.delay(sender, instance.id, created)
