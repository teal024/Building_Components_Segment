from django.db import models

class UploadBatch(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"UploadBatch {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class OriginalImage(models.Model):
    image = models.ImageField(upload_to='images/')
    batch = models.ForeignKey(UploadBatch, on_delete=models.CASCADE, related_name='images')     # related_name 用于反向查询，这样后端可以知道一个 uploadBatch 对应的 images
    number_in_batch = models.PositiveIntegerField()
    processed = models.BooleanField(default=False)  # 默认为未处理
    def __str__(self):
        return f"Image {self.number_in_batch} in {self.batch}"
    
class ImageSegment(models.Model):      # 碎片对应的表，里面存有图片源信息和对应的原图
    segment_source = models.ImageField(upload_to='segments/')
    original = models.ForeignKey(OriginalImage, on_delete=models.CASCADE, related_name='imageSegments')     # 可以找到一张原图片对应的 segment
    def __str__(self):
        return f"ImageSegments {self.id} of {self.original}"
