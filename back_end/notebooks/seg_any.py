import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import sys
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware #解决跨域问题
import shutil
from pathlib import Path
import io
from fastapi.responses import JSONResponse
import os
sys.path.append("..")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

path1 = 'images/dog.jpg'
path2 = r'C:\Users\23011\Desktop\vue_test28\ldk_new\src\assets\result\1.png'

def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)

def sam(image_path):


# plt.figure(figsize=(20,20))
# plt.imshow(image)
# plt.axis('off')
# plt.show()

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    sam_checkpoint = "../sam_vit_b_01ec64.pth"
    model_type = "vit_b"

    device = "cuda"

    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)

    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    result_string = f"The number of the segment result is {len(masks)}"

    plt.figure(figsize=(13, 13))
    plt.imshow(image)
    show_anns(masks)
    plt.axis('off')
    plt.savefig(path2)
    plt.show()
    abs_path = os.path.abspath(path2)
    return abs_path, result_string

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)

@app.post("/sam")
async def sam_process(file: UploadFile = File(...)):
    try:
        upload_folder = "uploaded_images"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        image_path = os.path.join(upload_folder, file.filename)
        with open(image_path, "wb") as f:
            f.write(file.file.read())


        output, msg = sam(image_path)

        return JSONResponse(content={"message": msg, "output": output})
    except Exception as e:
        return JSONResponse(content={"message": "Error uploading image", "error": str(e)})


if __name__ == "__main__":
    uvicorn.run(app)
