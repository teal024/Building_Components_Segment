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


def segment_image(input_image_data, output_dir='backend/media/segged', sam_checkpoint="backend/sam_vit_h_4b8939.pth",
                  model_type="vit_h"):
    # 清空output_dir里的内容
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
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
    height = int(image.shape[0] * 25 / 100)
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
            if ann['area'] > size / 36 and ann['area'] < size / 2:
                print(ann['area'])
                img_tosave = np.where(m[..., None] == 1, original_image, 255)
                img_tosave = cv2.cvtColor(img_tosave, cv2.COLOR_BGR2RGB)
                # img_tosave 送进分类器
                # 返回值是一个label
                label = classify(img_tosave)
                # 数据整合在一起
                output_filename = f"{index}_saved_{label}.png"
                output_path = os.path.join(output_dir, output_filename)
                cv2.imwrite(output_path, img_tosave)

    generate_anns(masks, image, size)


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
