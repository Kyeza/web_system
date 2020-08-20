import logging

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from payroll.models import EarningDeductionType, PayrollCenterEds, PayrollCenter
from users.models import DisplayIdCounter

logger = logging.getLogger('payroll')


@receiver(post_save, sender=EarningDeductionType)
def add_display_number_to_enumeration(sender, instance, created, **kwargs):
    if created:
        if instance.usable == 'YES':

            # set display id for enumeration
            display_id_setter = DisplayIdCounter.load()

            curr = display_id_setter.current_id
            instance.display_number = curr + 1
            instance.usable = 'NO'
            instance.save()
            display_id_setter.current_id = instance.display_number
            display_id_setter.previous_id = curr
            display_id_setter.save()

            # add an enumeration to Payroll center specific enumerations
            for payroll_center in PayrollCenter.objects.all():
                PayrollCenterEds.objects.create(ed_type_id=instance.id,
                                                payroll_center_id=payroll_center.id)

            logger.info(f'new enumeration {instance} has successfully been added')

# TODO: Please implement the post delete and implement logic to reduce the display ids count once an enumeration
#  a display id not 1001 has been deleted
