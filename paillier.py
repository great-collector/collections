from Crypto.Util import number
import random
from math import gcd,lcm
import math

def L(x, n):
    return (x - 1) // n

class paillier:
    def __init__(self):
        n,g,lam,u=self.get_args()
        self.n=n
        self.g=g
        self.lam=lam
        self.u=u

    def get_args(self):
        while True:
            p=number.getPrime(1024)
            q=number.getPrime(1024)
            if gcd(p * q, (p - 1) * (q - 1)) == 1:
                break
        n=p*q
        lam=lcm(p-1,q-1)
        g=n+1
        x = pow(g, lam, n*n)
        u = pow(L(x,n), -1, n)
        return n,g,lam,u
    
    def enc(self,m):
        r=random.randint(1,self.n-1)
        n2=self.n*self.n
        c=(pow(self.g, m, n2) * pow(r, self.n, n2))%n2
        return c

    def dec(self,c):
        m=pow(L(pow(c,self.lam,self.n*self.n),self.n)*self.u,1,self.n)
        return m
    
def compute_inner_product(vector_a, vector_b_encrypted, n_square):
    if len(vector_a) != len(vector_b_encrypted):
        raise ValueError("向量长度不匹配")
    
    result = 1
    for a_i, b_i in zip(vector_a, vector_b_encrypted):
        # 利用同态性质: E(m1)^a * E(m2)^b = E(m1*a + m2*b)
        result = (result * pow(b_i, a_i, n_square)) % n_square
    return result


def get_similar(a_b_inner,a_plain,b_plain):
    a_plain = [int(round(x)) for x in a_plain]
    b_plain = [int(round(x)) for x in b_plain]
    norm_a = math.sqrt(sum(x * x for x in a_plain))
    norm_b = math.sqrt(sum(x * x for x in b_plain))

    if norm_a == 0 or norm_b == 0:
        raise ValueError("其中一个向量是零向量，无法计算余弦相似度")
    cosine_sim = a_b_inner / (norm_a * norm_b)
    return cosine_sim

def mse(a, b):
    if len(a) != len(b):
        raise ValueError("两个向量长度必须一致")
    
    diff_sum = 0
    for x, y in zip(a, b):
        diff_sum += (x - y) ** 2
    
    return diff_sum / len(a)
