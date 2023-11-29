from django.db import models

class BatchUpload(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch Upload {self.id}"

class Image(models.Model):
    BATCH_CHOICES = [
        ('A', 'segmentation'),
        ('B', 'explosion_identify')
    ]

    func = models.CharField(blank=False, null=False, max_length=100, choices=BATCH_CHOICES)
    image = models.ImageField(upload_to='uploads/')
    batch_upload = models.ForeignKey(BatchUpload, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name