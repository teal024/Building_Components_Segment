import io
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from backend.models import Image
from rest_framework import status
from backend.serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings

import os
import numpy as np
import cv2
from backend.tools import segment_image
import re


class GetImg(GenericViewSet):
    @action(methods=['post'], detail=False)
    def save_image(self, request):
        file_path = './backend/media/' # 指定保存文件的文件夹路径
        # 若文件夹不存在则新建
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        if request.POST.get('func')  == 'A':
            file_path = os.path.join(file_path,'segmentaion')
            try:
                uploaded_file = request.FILES['image']  # 获取上传的图像文件
                FileSystemStorage(location=file_path)
                # 读取上传的图像文件并转换为numpy数组
                image_data = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

                # 调用图像分割函数进行处理
                segment_image(image_data)

                image_list = []  # 用于存储图片路径的列表
                label_list = []
                valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']  # 允许的图片文件扩展名列表

                # 遍历文件夹中的所有文件和子文件夹
                for root, dirs, files in os.walk('./backend/media/segged'):
                    for file in files:
                        file_extension = os.path.splitext(file)[1].lower()  # 获取文件扩展名并转换为小写
                        if file_extension in valid_extensions:
                            image_path = request.build_absolute_uri('/media/segged/' + file)
                            image_list.append(image_path)
                            filename, _ = os.path.splitext(file)
                            # 使用正则表达式提取标签
                            match = re.search(r'[^_]+$', filename)  # 匹配最后一个下划线之后的部分
                            if match:
                                label = match.group()
                                label_list.append(label)
                            else:
                                label_list.append(None)  # 如果没有匹配到标签，可以添加一个默认值或者处理方式

                return Response({'message': 'Image processing complete.',
                                 'total': len(image_list),  #结果图片数量
                                 'pictures': image_list,
                                 'labels': label_list,
                                 },
                                 status = status.HTTP_200_OK)
            except Exception as e:
                print(e)
                # 处理异常情况
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UploadCsv(GenericViewSet):
    @action(methods=['post'], detail=False)
    def save_csv(self,request):
        file_path = './backend/media/' # 指定保存文件的文件夹路径

        file_path = os.path.join(file_path,'vibration')
        # 若文件夹不存在则新建
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        try:
            uploaded_file = request.FILES['csv']  # 获取上传的图像文件

            # 创建文件系统存储对象
            fs = FileSystemStorage(location=file_path)
            fs.save(uploaded_file.name, uploaded_file)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
