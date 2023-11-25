from argparse import _ActionsContainer
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
import torch
import cv2
import sys

from backend.segment_anything import sam_model_registry, SamAutomaticMaskGenerator

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
                valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']  # 允许的图片文件扩展名列表
    
                # 遍历文件夹中的所有文件和子文件夹
                for root, dirs, files in os.walk('./backend/media/segged'):
                    for file in files:
                        file_extension = os.path.splitext(file)[1].lower()  # 获取文件扩展名并转换为小写
                        if file_extension in valid_extensions:
                            image_path = request.build_absolute_uri('/media/segged/' + file)
                            image_list.append(image_path)
     
                return Response({'message': 'Image processing complete.',
                                 'total': len(image_list),  #结果图片数量
                                 'pictures':image_list},
                                 status=status.HTTP_200_OK)
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

def segment_image(input_image_data, output_dir='backend/media/segged', sam_checkpoint="backend/sam_vit_h_4b8939.pth", model_type="vit_h"):
    # 清空output_dir里的内容
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    # Check if CUDA is available
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print("here")
    
    # Load the SAM model
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)

    # Process the input image data
    image = cv2.cvtColor(input_image_data, cv2.COLOR_BGR2RGB)
    width = int(image.shape[1] * 25 / 100)
    height = int(image.shape[0]* 25 / 100)
    size = width * height
    image = cv2.resize(image, (width, height))
    masks = mask_generator.generate(image)

    def generate_anns(anns, image, size):
        original_image = image
        if len(anns) == 0:
            return

        sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
        img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
        img[:, :, 3] = 0

        for index, ann in enumerate(sorted_anns):
            m = ann['segmentation']
            if ann['area'] > size / 36:
                print(ann['area'])
                img_tosave = np.where(m[..., None] == 1, original_image, 255)
                img_tosave = cv2.cvtColor(img_tosave, cv2.COLOR_BGR2RGB)
                output_filename = f"{index}_saved.png"
                output_path = os.path.join(output_dir, output_filename)
                cv2.imwrite(output_path, img_tosave)

    generate_anns(masks, image, size)
