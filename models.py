from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)