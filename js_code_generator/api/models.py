from django.db import models

class Script(models.Model):
    function_name = models.CharField(max_length=300)
    script_content = models.CharField(max_length=5000)
    def __str__(self):
        return self.function_name