from argparse import _ActionsContainer
from rest_framework.response import Response
from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from backend.models import Image

from backend.serializers import ImageSerializer

# Create your views here.
class GetImg(GenericViewSet):
    serializer_class = ImageSerializer

    # 保存图片
    @action(methods=['post'], detail=False)
    def save_image(self, request):
        file = request.FILES.get('image')
        
        try:
            response = {'code': 200, 'msg': "后端连接成功"}

            #！！下面代码会出bug，需要修改才能保存文件！！
        #     # 保存文件
        #     file_path = './backend/media/img/' + file.name
        #     with open(file_path, 'wb+') as f:
        #         f.write(file.read())
        #         f.close()

        #     # 创建 Image 对象并保存
        #     image = Image.objects.create(file=file_path, name=file.name, size=file.size)
        #     serializer = self.get_serializer(image)
        #     response = {'file': serializer.data, 'code': 200, 'msg': "添加成功"}
        except:
             response = {'file': file, 'code': 201, 'msg': "连接失败"}
        return Response(response)
    
    @action(methods=['get'], detail=False)
    def layer():
        print(111)
