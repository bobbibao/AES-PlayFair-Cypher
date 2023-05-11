import numba


class CTR:
    def __init__(self, cipher, nonce):
        self.cipher = cipher
        self.nonce = nonce

    @staticmethod
    @numba.jit(nopython=True)
    def _xor(data_1, data_2):
        return [a ^ b for a, b in zip(data_1, data_2)]

    def encrypt(self, data_block, counter):
        counter_bytes = counter.to_bytes(6, byteorder="big")
        IV = self.nonce + counter_bytes
        ciphertext = bytes(self._xor(self.cipher.encrypt(IV), data_block))
        return ciphertext

    def decrypt(self, cipher_block, counter):
        return self.encrypt(cipher_block, counter)
