import io
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from backend.models import *
from rest_framework import status
from backend.serializers import *
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
from PIL import Image
from django.core.files.base import ContentFile
from datetime import date


·
import os
import numpy as np
import cv2
from backend.my_tools import segment_image
import re
from rest_framework.parsers import MultiPartParser, FormParser
import base64


class ImgActions(GenericViewSet):       # 一个大类，表示所有与图像有关的 api
    parser_classes = (MultiPartParser, FormParser)

    # API 0
    @action(methods=['post'], detail=False)
    def seg_single_image(self, request):
        print("in the seg_single_image method")
        try:
            uploaded_file = request.FILES['image']  # 获取上传的图像文件
            # 读取上传的图像文件并转换为numpy数组
            image_data = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # 调用图像分割函数进行处理
            segmented_images = segment_image(image_data)  # 修改segment_image函数返回分割后的图像列表

            image_list = []
            label_list = []

            file_path = os.path.join(settings.MEDIA_ROOT, 'segged')
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            else:   # 清除这个文件夹里面的内容
                for filename in os.listdir(file_path):
                    file = os.path.join(file_path, filename)
                    if os.path.isfile(file):
                        os.remove(file)


            for index, segmented_pair in enumerate(segmented_images):
                segmented_image = segmented_pair['image']
                segmented_label = segmented_pair['label']
                
                # 将numpy数组转换为PIL Image
                segmented_pil_image = Image.fromarray(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
                
                # 将PIL Image保存到路径中
                file_name = 'image_{0}.jpg'.format(index)
                image_file_path = os.path.join(file_path, file_name)
                segmented_pil_image.save(image_file_path, format='JPEG')

                image_path = request.build_absolute_uri('/media/segged/' + file_name)
                # 构建图像路径
                image_list.append(image_path)
                label_list.append(segmented_label)

            return Response({'message': 'Image processing complete.',
                             'total': len(image_list),  # 结果图片数量
                             'pictures': image_list,
                             'labels': label_list,
                             },
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # API 1 管理员上传多张图片，后端存储到数据库中，返回图片ID和对应批次号，以及这个批次的时间
    @action(methods=['post'], detail=False)
    def upload_batch_image(self, request):
        print("in the upload_batch_image method")
        try:
            uploaded_files = request.FILES.getlist('image')  # 获取上传的多个图像文件

            # 创建一个新的 Batch 对象
            batch = UploadBatch.objects.create()
            image_list = []

            for i, uploaded_file in enumerate(uploaded_files):
                # 创建 OriginalImage 对象并将其关联到新创建的 Batch 对象
                image = OriginalImage(image=uploaded_file, batch=batch, number_in_batch=i + 1)
                image.save()
                image_list.append(image.id)

            return Response({'message': 'Images uploaded successfully.',
                             'images': image_list,
                             'batch_id': batch.id,
                             'batch_time': batch.created_at},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # API 2 管理员发送带ID的请求，后端处理相应图片并返回是否成功，处理结果共有多少张，并返回一个标签列表，前端可以做个类似于“成功分割，分割出了xx张图片，其中有xx张xx,xx张xx"这样的提示
    @action(methods=['post'], detail=False)
    def seg_single_image_from_to_db(self, request):
        print("in the seg_single_image_from_to_db method")
        try:
            image_id = request.data.get('image_id')  # 获取请求中的图像ID
            original_image = OriginalImage.objects.get(id=image_id)  # 从数据库中获取原始图像对象
            if original_image.processed == False:
                # 读取原始图像数据并转换为numpy数组
                image_data = cv2.imdecode(np.fromstring(original_image.image.read(), np.uint8), cv2.IMREAD_COLOR)

                # 调用图像分割函数进行处理
                segmented_images = segment_image(image_data)  # 修改segment_image函数返回分割后的图像列表

                # 处理完成
                original_image.processed = True
                original_image.save()

                label_list = []

                for index, segmented_pair in enumerate(segmented_images):
                    segmented_image = segmented_pair['image']
                    segmented_label = segmented_pair['label']

                    # 创建ImageSegments对象并将其关联到原始图像对象
                    image_segment = ImageSegment(original=original_image)
                    # 将分割图像数据保存到 imageSegments 字段中
                    image_segment.segment_source.save(f'segments/image_segged_from_{image_id}_{index}.jpg', ContentFile(cv2.imencode('.jpg', segmented_image)[1].tobytes()), save=False)
                    # 保存 ImageSegments 实例到数据库
                    image_segment.save()
                    
                    label_list.append(segmented_label)

                return Response({'message': 'Image processing complete.',
                                'total': len(segmented_images),  # 结果图片数量
                                'label_list': label_list,
                                },
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'The image is already in the database.',
                                },
                                status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # API 3：管理员发送带ID的请求，后端从数据库中查询到对应图片并返回分割和分类结果
    @action(methods=['post'], detail=False)
    def get_segmented_images_for_image(self, request):
        try:
            image_id = request.data.get('image_id')  # Get the image_id from the request
            original_image = OriginalImage.objects.get(id=image_id)  # Retrieve the OriginalImage using image_id
            if original_image.processed == True:
                # Use the related_name 'imageSegments' to get segmented images
                segmented_images = original_image.imageSegments.all()

                # Extract file paths from segmented_images
                segment_paths = [segment.segment_source.url for segment in segmented_images]

                return Response({'message': 'Segmented image paths retrieved successfully.',
                                'segmented_image_paths': segment_paths},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Original image not segged.'}, status=status.HTTP_404_NOT_FOUND)

        except OriginalImage.DoesNotExist:
            return Response({'error': 'Original image not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    # API 4：根据日期查询数据库中的图片（返回当日所有图片）
    @action(methods=['post'], detail=False)
    def get_all_image(self, request):
        print("in the get_all_image method")
        try:
            # 获取传递的日期参数
            date_str = request.data.get('date')

            # 解析日期字符串为日期对象
            query_date = date.fromisoformat(date_str)

            # 使用Q对象组合查询条件
            # 获取指定日期上传的批次
            batches = UploadBatch.objects.filter(
                created_at__date=query_date
            )

            # 初始化存储结果的列表
            images_data = []

            # 遍历每个批次，获取对应的图片信息
            for batch in batches:
                images_in_batch = batch.images.all()
                for image in images_in_batch:
                    # 构建每张图片的数据
                    image_data = {
                        'id': image.id,
                        'image_url': image.image.url,
                    }
                    images_data.append(image_data)

            return JsonResponse({'message': 'Images retrieved successfully.',
                                 'images': images_data},
                                status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            # 处理异常情况
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    

   
