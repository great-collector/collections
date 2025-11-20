from paillier import *
import random
import time

N = 100
Q=[random.randint(0, 255) for _ in range(10)]
vectors = [[random.randint(0, 255) for _ in range(10)] for _ in range(N)]

start_init = time.time()
paillier = paillier()
init_time = time.time() - start_init

start_encrypt = time.time()
encrypted_Q = [paillier.enc(x) for x in Q]
encrypt_time = time.time() - start_encrypt

decrypt_times=[]
compute_times=[]
similars=[]
mses=[]
for vector in vectors:    
    start_compute = time.time()
    encrypted_result = compute_inner_product(vector, encrypted_Q, paillier.n**2) #内积
    
    start_decrypt = time.time()
    result = paillier.dec(encrypted_result)
    decrypt_time = time.time() - start_decrypt
    decrypt_times.append(decrypt_time)
    
    similar=get_similar(result,Q,vector)
    similars.append(similar)
    _mse=mse(Q,vector)
    mses.append(_mse)
    compute_time = time.time() - start_compute-decrypt_time
    compute_times.append(compute_time)
    
max_similar = max(similars)
index = similars.index(max_similar)

avg_compute_time=sum(compute_times)/len(compute_times)
avg_decrypt_time=sum(decrypt_times)/len(decrypt_times)

print(f"\n=== Paillier方案性能测试 ===")
print(f"向量Q: {Q}")
print(f"最匹配向量: {vectors[index]}")
print(f"内积结果: {result}")
print(f"相似度:{max_similar}")
print(f"MSE:{mses[index]}")

print(f"\n运行时间统计:")
print(f"密钥初始化时间: {init_time:.4f} 秒")
print(f"加密时间: {encrypt_time:.4f} 秒")
print(f"平均计算时间: {avg_compute_time:.4f} 秒")
print(f"平均解密时间: {avg_decrypt_time:.4f} 秒")

    