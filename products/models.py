from django.db import models
from django.contrib.auth.models import User
    
class Products(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.TextField()
    price = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title

