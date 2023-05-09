from flask import Flask, request, render_template, jsonify
from Crypto.Cipher import AES
import base64
from flask.views import MethodView
from flask import url_for

app = Flask(__name__)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

class AESCipher(MethodView):
    def post(self, operation):
        key = request.form['key']
        data = request.form['data']
        iv = b'0000000000000000'
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        
        if operation == "encrypt":
            padded_data = data + (AES.block_size - len(data) % AES.block_size) * chr(AES.block_size - len(data) % AES.block_size)
            encrypted_data = cipher.encrypt(padded_data.encode('utf-8'))
            result = base64.b64encode(encrypted_data).decode('utf-8')
            
        elif operation == "decrypt":
            encrypted_data = base64.b64decode(request.form['data'])
            decrypted_data = cipher.decrypt(encrypted_data).decode('utf-8')
            padded_length = ord(decrypted_data[-1])
            decrypted_data = decrypted_data[:-padded_length]
            result = decrypted_data
        
        return jsonify({
            'result': result
        })
class PlayfairCipher(MethodView):
    
    def create_matrix(self, key):
        # Tạo ma trận khóa từ chuỗi key
        key = key.upper()
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
        #Trả về vị trí của một kí tự trong ma trận
        for i in range (5):
            try:
                index = matrix[i].index(letter)
                return (i,index)
            except:
                continue
    
    def playfair_cipher(self, key, message, encrypt=True):
        #Thực hiện mã hóa hoặc giải mã thông điệp đầu vào bằng Playfair Cipher theo khóa key được cung cấp.
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
        #Nhận thông tin từ form và trả về kết quả mã hóa hoặc giải mã
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
