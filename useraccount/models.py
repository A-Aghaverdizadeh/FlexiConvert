from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users')
    delete_image = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.delete_image and self.image:
            self.image.delete(save=False)
            self.image = None
            self.delete_image = False  # Reset the flag
        super().save(*args, **kwargs)

