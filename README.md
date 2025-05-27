AES - Mã hóa & Giải mã File

Ứng dụng web đơn giản dùng Flask để mã hóa và giải mã file bằng thuật toán AES (chế độ ECB). Hỗ trợ nhập mật khẩu, tải file lên để mã hóa hoặc giải mã và tải file kết quả xuống.

Tính năng:

Mã hóa file bất kỳ với mật khẩu do người dùng nhập.

Giải mã file .aes với mật khẩu đúng.

Giao diện web thân thiện, hiện đại dùng Bootstrap 5.

Hiển thị thông báo lỗi và thành công rõ ràng.

Tự động mở trình duyệt khi chạy ứng dụng.

Yêu cầu:

Python 3.7 trở lên

Các thư viện cần cài đặt:

pip install flask pycryptodome

Cách sử dụng:

Clone hoặc tải mã nguồn về máy.

Cài đặt thư viện:

pip install flask pycryptodome

Chạy ứng dụng:

python app.py

Ứng dụng sẽ tự động mở trình duyệt trên địa chỉ http://127.0.0.1:5000

Sử dụng tab Mã hóa để chọn file cần mã hóa và nhập mật khẩu, nhấn nút Mã hóa để tải file .aes về.

Sử dụng tab Giải mã để chọn file .aes đã mã hóa và nhập mật khẩu đúng, nhấn Giải mã để tải file gốc về.

Lưu ý:

Mật khẩu được băm bằng SHA-256 để tạo khóa AES.

AES sử dụng chế độ ECB (dễ hiểu, demo, không an toàn trong thực tế).

File mã hóa chứa tên file gốc và băm mật khẩu để kiểm tra khi giải mã.

Mật khẩu không được để trống.

Sai mật khẩu hoặc file lỗi sẽ hiển thị thông báo lỗi.

Cấu trúc chính

app.py: chứa toàn bộ logic Flask, mã hóa, giải mã.

HTML, CSS được nhúng sẵn trong biến HTML.

Các route chính:

/: trang giao diện chính.

/encrypt: xử lý mã hóa file.

/decrypt: xử lý giải mã file.

Mở rộng đề xuất:

Thay chế độ AES ECB thành CBC với IV cho an toàn hơn.

Giới hạn kích thước file.

Lưu lịch sử mã hóa/giải mã.

Cải thiện giao diện và trải nghiệm người dùng.

Giao diện web:

Mã hóa:
 ![image](https://github.com/user-attachments/assets/e0f7d7b3-f178-404b-871a-b7a2736fe225)


Giải mã:
 ![image](https://github.com/user-attachments/assets/89dbfa3d-41e5-4a91-a671-a1fa556d0882)

