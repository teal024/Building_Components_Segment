from argparse import _ActionsContainer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from backend.models import Image
from rest_framework import status
from backend.serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

import os
import numpy as np
import torch
import cv2
import sys
# 模块路径添加到 sys.path
#sys.path.append('/root/StudyOnCurtainWall/backend')
from backend.segment_anything import sam_model_registry, SamAutomaticMaskGenerator

# Create your views here.
class GetImg(GenericViewSet):
    serializer_class = ImageSerializer

    @action(methods=['get'], detail=False)
    def layer(self):
        print('get something')


    @action(methods=['post'], detail=False)
    def save_image(self, request):
        try:
            uploaded_file = request.FILES['image']  # 获取上传的图像文件

            # 读取上传的图像文件并转换为numpy数组
            image_data = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

            # 调用图像分割函数进行处理
            segment_image(image_data)
            return Response({'message': 'Image processing complete.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            # 处理异常情况
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def segment_image(input_image_data, output_dir='/root/StudyOnCurtainWall/backend/segged', sam_checkpoint="/root/StudyOnCurtainWall/backend/sam_vit_h_4b8939.pth", model_type="vit_h"):
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
            if ann['area'] > size / 24 and ann['area'] < size / 2:
                img_tosave = np.where(m[..., None] == 1, original_image, 255)
                img_tosave = cv2.cvtColor(img_tosave, cv2.COLOR_BGR2RGB)
                output_filename = f"{index}_saved.png"
                output_path = os.path.join(output_dir, output_filename)
                cv2.imwrite(output_path, img_tosave)

    generate_anns(masks, image, size)
