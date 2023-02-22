from django.db.models.signals import post_save
# after register Profile will be automatically created for this we are using this file
from django.contrib.auth.models import User # Sender - For Sending the Signals
# We Will create a Receiver function - to perform some task on the signals
from django.dispatch import receiver
from . models import Profile


@receiver(post_save, sender = User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
def saveProfile(sender, instance, **kwargs):
    instance.profile.save()



# The code will then use the receiver decorator to register this function with the post_save signal.
# The sender parameter in this case is User which means that any user who sends the post_save signal will trigger this function.
# This function will be called after every new user has been created and it will perform some task on the signals.