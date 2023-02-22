# Import the necessary models from Django 
from django.db import models
from django.contrib.auth.models import User

# Import Image module from PIL library
from PIL import Image

# Define the Profile model which is a sub-model of the User model
class Profile(models.Model):

    # Connects the User model with the Profile model through a OneToOne relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The image field is used to store the profile picture of the user
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    # Return a string representation of the profile which is the username of the user
    def __str__(self):
        return f'{self.user.username} Profile'

    # Save method to reduce the size of the uploaded image
    def save(self, **kwargs):

        # Call the save method on the parent class (models.Model)
        super().save()
        img = Image.open(self.image.path)

        # Check the height and width of the image; if it exceeds 300 pixels resize it
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
