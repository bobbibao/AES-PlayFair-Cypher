from flask import Flask, request, render_template, jsonify
import secrets, hmac, hashlib, base64
from flask.views import MethodView
from aes import AES
from ctr import CTR

app = Flask(__name__)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

class AESCipher(MethodView):
    def post(self, operation):
        key = request.form['key']
        data = request.form['data']
        block_size = 16
        def encrypt_decrypt(func, in_stream, block_size, count_start):
            return b"".join(
                [
                    func(in_stream[i : i + block_size], i // block_size + count_start)
                    for i in range(0, len(in_stream), block_size)
                ]
            )
        if operation == "encrypt":
            plaintext = bytes(data, encoding='utf-8')
            passwd = key
            salt = secrets.token_bytes(block_size)
            nonce = secrets.token_bytes(10)
            counter = 0
            IV = nonce + counter.to_bytes(6, "big")
            cipher = AES(password_str=passwd, salt=salt, key_len=256)
            mode = CTR(cipher, nonce)
            result = (
                salt + IV + encrypt_decrypt(mode.encrypt, plaintext, block_size, counter)
            )
            hmac_val = hmac.digest(key=cipher.hmac_key, msg=result, digest=hashlib.sha256)
            result += hmac_val
            result = base64.b64encode(result).decode("utf-8")

        elif operation == "decrypt":
            file_in = base64.b64decode(data)
            passwd = key

            salt = file_in[0:block_size]
            nonce = file_in[block_size : block_size + 10]

            counter = file_in[block_size + 10 : block_size + 10 + 6]
            counter = int.from_bytes(counter, "big")

            hmac_val = file_in[-2 * block_size :]
            cipher = AES(password_str=passwd, salt=salt, key_len=256)

            assert hmac.compare_digest(
                hmac_val,
                hmac.digest(
                    key=cipher.hmac_key,
                    msg=file_in[: -2 * block_size],
                    digest=hashlib.sha256,
                ),
            ), "HMAC check failed."

            mode = CTR(cipher, nonce)
            file_in = file_in[2 * block_size : -2 * block_size]
            result = encrypt_decrypt(mode.decrypt, file_in, block_size, counter).decode('utf-8')
        return jsonify({
            'result': result
        })
class PlayfairCipher(MethodView):
    
    def create_matrix(self, key):
        # Tạo ma trận khóa từ chuỗi key
        key = key.upper()
        base64.encode
        matrix = [[0 for i in range(5)] for j in range(5)]
        letters_added = []
        row = 0
        col = 0

        # Thêm các kí tự trong key vào ma trận
        for letter in key:
            if letter not in letters_added:
                matrix[row][col] = letter
                letters_added.append(letter)
            else:
                continue
            if (col==4):
                col = 0
                row += 1
            else:
                col += 1
        
        #Thêm các kí tự còn lại của bảng chữ cái vào ma trận
        for letter in range(65,91):
            if letter==74: # I/J are in the same position
                    continue
            if chr(letter) not in letters_added:
                letters_added.append(chr(letter))

        index = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = letters_added[index]
                index+=1
        return matrix
    
    def separate_same_letters(self, message):
        #Thêm kí tự "X" nếu hai kí tự giống nhau đứng cùng vị trí trong tin nhắn
        index = 0
        while (index<len(message)):
            l1 = message[index]
            if index == len(message)-1:
                message = message + 'X'
                index += 2
                continue
            l2 = message[index+1]
            if l1==l2:
                message = message[:index+1] + "X" + message[index+1:]
            index +=2   
        return message
    
    def indexOf(self, letter,matrix):
        for i in range (5):
            try:
                index = matrix[i].index(letter)
                return (i,index)
            except:
                continue
    
    def playfair_cipher(self, key, message, encrypt=True):
        inc = 1
        if encrypt==False:
            inc = -1
        matrix = self.create_matrix(key)
        message = message.upper()
        message = message.replace(' ','')    
        message = self.separate_same_letters(message)
        cipher_text=''
        for (l1, l2) in zip(message[0::2], message[1::2]):
            row1,col1 = self.indexOf(l1,matrix)
            row2,col2 = self.indexOf(l2,matrix)
            if row1==row2: #Rule 2, the letters are in the same row
                cipher_text += matrix[row1][(col1+inc)%5] + matrix[row2][(col2+inc)%5]
            elif col1==col2:# Rule 3, the letters are in the same column
                cipher_text += matrix[(row1+inc)%5][col1] + matrix[(row2+inc)%5][col2]
            else: #Rule 4, the letters are in a different row and column
                cipher_text += matrix[row1][col2] + matrix[row2][col1]

        return cipher_text
    
    def post(self, operation):
        key = request.form['key']
        message = request.form['data']
        
        if operation == 'encrypt':
            result = self.playfair_cipher(key, message)
        elif operation == 'decrypt':
            result = self.playfair_cipher(key, message, False)
        else:
            result = "Invalid operation"
            
        return jsonify({
            'result': result
        })
    
# Routes
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/aes/<string:operation>', view_func=AESCipher.as_view('AESCipher'))
app.add_url_rule('/playfair/<string:operation>', view_func=PlayfairCipher.as_view('PlayfairCipher'))


if __name__ == '__main__':
    app.run()
