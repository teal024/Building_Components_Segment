from argparse import _ActionsContainer
from rest_framework.response import Response
from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from backend.models import Image

from backend.serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage

import os


# Create your views here.
class GetImg(GenericViewSet):
    serializer_class = ImageSerializer

    # 保存图片
    @action(methods=['post'], detail=False)
    def save_image(self, request):
        file = request.FILES.get('image')
        print(file)

        file_path = './backend/media/' # 指定保存文件的文件夹路径

        # 若文件夹不存在则新建
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_path = os.path.join(file_path,'img')

        fs = FileSystemStorage(location=file_path)
        try:
            filename = fs.save(file.name, file)

            response = {'file':filename, 'code': 200, 'msg': '图片保存成功'}
        except:
             response = {'file': file, 'code': 201, 'msg': "连接失败"}
        return Response(response)

    @action(methods=['get'], detail=False)
    def layer(self):
        print(111)
