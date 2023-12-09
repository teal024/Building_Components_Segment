from backend.segment_anything import sam_model_registry, SamAutomaticMaskGenerator
import os
import numpy as np
import torch
import cv2
import torchvision.transforms as transforms
import torch.nn.functional as F
from torch.autograd import Variable

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

model = torch.load("backend/best_model.pth")
model.eval()
model.to(device)
classes = ('金属', '玻璃', '其它')


def segment_image(input_image_data, sam_checkpoint="backend/sam_vit_h_4b8939.pth",
                  model_type="vit_h"):
    print("here in the segment process, loading...")
    # 创建一个用于存储分割图片和标签的列表
    segmented_images = []

    # Load the SAM model
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)

    # Process the input image data
    image = cv2.cvtColor(input_image_data, cv2.COLOR_BGR2RGB)
    width = int(image.shape[1] * 25 / 200)
    height = int(image.shape[0] * 25 / 200)
    size = width * height
    image = cv2.resize(image, (width, height))
    masks = mask_generator.generate(image)

    original_image = image
    if len(masks) == 0:
        return segmented_images

    sorted_anns = sorted(masks, key=(lambda x: x['area']), reverse=True)

    for index, ann in enumerate(sorted_anns):
        m = ann['segmentation']
        if ann['area'] > size / 36 and ann['area'] < size / 2:
            img_tosave = np.where(m[..., None] == 1, original_image, 255)
            img_tosave = cv2.cvtColor(img_tosave, cv2.COLOR_BGR2RGB)
            # img_tosave 送进分类器
            # 返回值是一个label
            label = classify(img_tosave)
            # 将分割图片和标签添加到列表中
            segmented_images.append({'image': img_tosave, 'label': label})

    return segmented_images


def transform_test(image):
    transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224)),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])
    return transform(image)


def classify(image):
    img = transform_test(image)
    img.unsqueeze_(0)
    img = Variable(img).to(device)
    out = model(img)
    # 获取预测的类别
    _, pred = torch.max(out.data, 1)
    return classes[pred.data.item()]
