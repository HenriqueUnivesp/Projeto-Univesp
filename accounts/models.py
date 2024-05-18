from django.db import models

# Create your models here.


class Usuario(models.Model):
    register_prefeitura = models.CharField(max_length=50)
    coluna_1234 = models.CharField(max_length=50)
    