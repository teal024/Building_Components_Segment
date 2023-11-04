from django.db import models

# Create your models here.
class Image(models.Model):
    uid = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)
    file_path = models.FileField(upload_to='uploads/')

    class Meta:
        app_label = 'backend'
    def __str__(self):
        return self.name