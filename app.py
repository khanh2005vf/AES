import webbrowser
import threading
from flask import Flask, request, send_file, render_template_string, flash, redirect, url_for
from Crypto.Cipher import AES
import hashlib
import struct
import os
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Mã hóa & Giải mã File bằng AES</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        /* CSS giữ nguyên */
        body {
            background:#8DEEEE;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #8DEEEE;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 600px;
        }
        .card {
            background: #ffffff;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            padding: 30px 40px;
        }
        h1 {
            font-weight: 700;
            text-align: center;
            margin-bottom: 20px;
            color: #34495e;
        }
        .nav-tabs .nav-link {
            color: #34495e;
            font-weight: 600;
            border: none;
            border-radius: 8px 8px 0 0;
            background: #ecf0f1;
            transition: background 0.3s, color 0.3s;
        }
        .nav-tabs .nav-link:hover {
            background: #d1dade;
            color: #2c3e50;
        }
        .nav-tabs .nav-link.active {
            background: #2980b9;
            color: #fff;
            font-weight: 700;
            box-shadow: 0 4px 15px rgba(41, 128, 185, 0.4);
        }
        label {
            font-weight: 600;
            color: #34495e;
        }
        .form-control {
            border-radius: 10px;
            border: 1.5px solid #bdc3c7;
            padding-left: 40px;
            transition: border-color 0.3s;
        }
        .form-control:focus {
            border-color: #2980b9;
            box-shadow: 0 0 8px 0 #2980b9aa;
        }
        .input-group-text {
            background: #2980b9;
            border-radius: 10px 0 0 10px;
            border: none;
            color: #fff;
        }
        .btn-primary, .btn-success {
            border-radius: 10px;
            font-weight: 700;
            padding: 10px 25px;
            box-shadow: 0 4px 15px rgba(41, 128, 185, 0.4);
            transition: background 0.3s, box-shadow 0.3s;
        }
        .btn-primary {
            background-color: #3498db;
            border: none;
        }
        .btn-primary:hover {
            background-color: #217dbb;
            box-shadow: 0 6px 20px #217dbbaa;
        }
        .btn-success {
            background-color: #e67e22;
            border: none;
            color: #fff;
        }
        .btn-success:hover {
            background-color: #c36b17;
            box-shadow: 0 6px 20px #c36b1788;
        }
        .alert {
            border-radius: 10px;
            font-weight: 600;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="card">
        <h1>🔐 AES - Mã hóa & Giải mã File</h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <ul class="nav nav-tabs" id="aesTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="encrypt-tab" data-bs-toggle="tab" data-bs-target="#encrypt" type="button" role="tab">Mã hóa</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="decrypt-tab" data-bs-toggle="tab" data-bs-target="#decrypt" type="button" role="tab">Giải mã</button>
            </li>
        </ul>

        <div class="tab-content mt-3" id="aesTabContent">
            <div class="tab-pane fade show active" id="encrypt" role="tabpanel">
                <form action="/encrypt" method="post" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="encryptFile" class="form-label">Chọn file để mã hóa</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="bi bi-file-earmark"></i></span>
                            <input type="file" class="form-control" name="file" id="encryptFile" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="encryptPassword" class="form-label">Mật khẩu</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="bi bi-key-fill"></i></span>
                            <input type="password" class="form-control" name="password" id="encryptPassword" required placeholder="Nhập mật khẩu">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">🔒 Mã hóa</button>
                </form>
            </div>
            <div class="tab-pane fade" id="decrypt" role="tabpanel">
                <form action="/decrypt" method="post" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="decryptFile" class="form-label">Chọn file đã mã hóa</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="bi bi-file-earmark-lock"></i></span>
                            <input type="file" class="form-control" name="file" id="decryptFile" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="decryptPassword" class="form-label">Mật khẩu đã sử dụng</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="bi bi-key"></i></span>
                            <input type="password" class="form-control" name="password" id="decryptPassword" required placeholder="Nhập mật khẩu">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-success w-100">🔓 Giải mã</button>
                </form>
            </div>
        </div>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

def pad(data):
    padding_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([padding_len] * padding_len)

def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]

def get_aes_key(password):
    return hashlib.sha256(password.encode()).digest()[:32]

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files.get('file')
    password = request.form.get('password', '')

    if not file or not password:
        flash("Thiếu file hoặc mật khẩu.", "danger")
        return redirect(url_for('index'))

    content = file.read()
    key = get_aes_key(password)
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(content)
    encrypted_data = cipher.encrypt(padded)

    filename = os.path.basename(file.filename).encode()
    filename_len = len(filename)
    pw_hash = hashlib.sha256(password.encode()).digest()

    final_data = struct.pack("B", filename_len) + filename + pw_hash + encrypted_data
    return send_file(io.BytesIO(final_data), download_name=file.filename + ".aes", as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files.get('file')
    password = request.form.get('password', '')

    if not file or not password:
        flash("Thiếu file hoặc mật khẩu.", "danger")
        return redirect(url_for('index'))

    try:
        data = file.read()
        filename_len = data[0]
        filename = data[1:1+filename_len]
        pw_hash = data[1+filename_len:1+filename_len+32]
        encrypted_data = data[1+filename_len+32:]

        if hashlib.sha256(password.encode()).digest() != pw_hash:
            flash("Sai mật khẩu!", "danger")
            return redirect(url_for('index'))

        key = get_aes_key(password)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(encrypted_data))

        return send_file(io.BytesIO(decrypted), download_name=filename.decode(), as_attachment=True)
    except Exception as e:
        flash(f"Lỗi giải mã: {str(e)}", "danger")
        return redirect(url_for('index'))

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False, port=5000)
