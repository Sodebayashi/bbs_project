from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

class Article(models.Model):
    content = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("bbs:detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return self.content

