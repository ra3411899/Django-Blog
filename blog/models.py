from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title Of The Post')
    content = models.TextField(verbose_name='Write About Post')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

     # Need to Configured - No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
     # This will used, when user creates any blog, or creating blog with author - derectly redirect it to the detail view
