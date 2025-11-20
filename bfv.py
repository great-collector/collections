import tenseal as ts

class BFV:
    def __init__(self, poly_modulus_degree=8192):
        context = ts.context(
            ts.SCHEME_TYPE.BFV,
            poly_modulus_degree=poly_modulus_degree,
            plain_modulus=536903681  # 2^29 - 2^21 + 1
        )
        
        context.generate_galois_keys()
        self.context = context

    def encrypt_vector(self, vector):
        # 确保输入向量的每个元素都是整数
        vector = [int(round(x)) for x in vector]  # 使用round确保正确转换
        return ts.bfv_vector(self.context, vector)

    def compute_dot_product(self, encrypted_vector, plain_vector):
        # 确保明文向量的每个元素都是整数
        plain_vector = [int(round(x)) for x in plain_vector]  # 使用round确保正确转换
        return encrypted_vector.dot(plain_vector)

    def decrypt_result(self, encrypted_result):
        # 返回解密结果
        decrypted = encrypted_result.decrypt()
        return decrypted[0] if isinstance(decrypted, list) else decrypted