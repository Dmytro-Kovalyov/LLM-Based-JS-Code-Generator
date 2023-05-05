from django.db import models

class Script(models.Model):
    script_content = models.CharField(max_length=5000)