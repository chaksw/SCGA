from django.db import models

# Create your models here.


class Scga(models.Model):
    file_name = models.TextField()
    baseline = models.TextField()

    def __str__(self):
        return self.title
