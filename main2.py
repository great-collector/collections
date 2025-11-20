from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from bfv import *
import time
from paillier import get_similar,mse
import os
import numpy as np
from PIL import Image

def pil_to_vector(img, size=(32, 32)):
    img = img.convert("RGB")      # 确保是 RGB
    img = img.resize(size)        # 调整大小
    arr = np.array(img)           # (H, W, 3)
    vector = arr.flatten().tolist()
    return vector

Q=Image.open("animal.jpg")
vector_Q=pil_to_vector(Q)

folder = "./photo"
images = []
for filename in os.listdir(folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):   # 过滤图片格式
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path)
        images.append(img)

start_init = time.time()
bfv = BFV()
init_time = time.time() - start_init

start_encrypt = time.time()
encrypted_Q = bfv.encrypt_vector(vector_Q)
encrypt_time = time.time() - start_encrypt

decrypt_times=[]
compute_times=[]
similars=[]
mses=[]
for img in images:
    
    start_compute = time.time()
    vector=pil_to_vector(img)
    encrypted_result = bfv.compute_dot_product(encrypted_Q, vector) #内积
    
    start_decrypt = time.time()
    result = bfv.decrypt_result(encrypted_result)
    decrypt_time = time.time() - start_decrypt
    decrypt_times.append(decrypt_time)
    
    similar=get_similar(result,vector_Q,vector)
    similars.append(similar)
    _mse=mse(vector_Q,vector)
    mses.append(_mse)
    compute_time = time.time() - start_compute-decrypt_time
    compute_times.append(compute_time)
    
max_similar = max(similars)
index = similars.index(max_similar)

avg_compute_time=sum(compute_times)/len(compute_times)
avg_decrypt_time=sum(decrypt_times)/len(decrypt_times)

print(f"\n=== BFV方案性能测试 ===")
fig, ax = plt.subplots(1, 2, figsize=(8, 4))

ax[0].imshow(Q)
ax[0].set_title("Query Image")
ax[0].axis('off')

ax[1].imshow(images[index])
ax[1].set_title("Matched Image")
ax[1].axis('off')

plt.show()


print(f"内积结果: {result}")
print(f"相似度:{max_similar}")
print(f"MSE:{mses[index]}")

print(f"\n运行时间统计:")
print(f"密钥初始化时间: {init_time:.4f} 秒")
print(f"加密时间: {encrypt_time:.4f} 秒")
print(f"平均计算时间: {avg_compute_time:.4f} 秒")
print(f"平均解密时间: {avg_decrypt_time:.4f} 秒")