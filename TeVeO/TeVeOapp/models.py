from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Camera(models.Model):

    source_id = models.CharField(max_length=100)
    id = models.CharField(max_length=100, primary_key=True)
    src = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100)
    img_path = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.source_id}{self.id} - {self.name}'


class Comment(models.Model):

    name = models.CharField(max_length=100)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    img_path_comment = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.camera} - {self.name} - {self.comment} - {self.date}'


class Token(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    font_size = models.CharField(max_length=200, null=True)
    font_family = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.user} - {self.token}'
