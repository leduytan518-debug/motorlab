# MOTORLAB – Thư viện kỹ thuật ô tô và xe máy

Ứng dụng web mẫu được xây dựng bằng Python, Flask, SQLite, HTML, CSS và JavaScript.

## 1. Yêu cầu
- Python 3.10 trở lên.
- Visual Studio Code.
- Kết nối Internet chỉ cần khi cài Flask lần đầu hoặc tải font Google Fonts. Các trang và dữ liệu chính vẫn chạy cục bộ sau khi đã cài thư viện.

## 2. Cài đặt trên Windows
Mở thư mục `garage_library` bằng VS Code, sau đó mở Terminal (Terminal → New Terminal) và chạy lần lượt:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Nếu PowerShell chặn kích hoạt môi trường ảo, có thể chạy lệnh sau trong cửa sổ Terminal hiện tại rồi kích hoạt lại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Nếu dùng Command Prompt (CMD), lệnh kích hoạt là:

```bat
.venv\Scripts\activate.bat
```

Sau khi thấy Flask báo máy chủ đang chạy, mở trình duyệt tại:

`http://127.0.0.1:5000`

Dừng máy chủ bằng `Ctrl + C` trong Terminal.

## 3. Cấu trúc thư mục

```text
garage_library/
│  app.py                 # Các đường dẫn và xử lý website
│  database.py            # Tạo SQLite và dữ liệu mẫu
│  requirements.txt       # Thư viện Python cần cài
│  README.md              # Hướng dẫn chạy
│
├─ instance/
│  └─ garage_library.db   # Tự tạo khi chạy lần đầu
│
├─ templates/             # Các trang HTML dùng Jinja2
│  ├─ base.html
│  ├─ index.html
│  ├─ vehicles.html
│  ├─ vehicle_detail.html
│  ├─ faults.html
│  ├─ parts.html
│  ├─ tools.html
│  ├─ prices.html
│  ├─ efi.html
│  └─ 404.html
│
└─ static/
   ├─ css/style.css       # Giao diện responsive
   └─ js/main.js          # Menu trên màn hình nhỏ
```

## 4. Chức năng hiện có
- Trang chủ, thống kê số lượng dữ liệu mẫu và lối tắt đến từng chuyên mục.
- Danh mục ô tô/xe máy, lọc theo loại và tìm kiếm theo hãng, dòng xe, động cơ.
- Trang chi tiết phương tiện, hiển thị nhóm lỗi và linh kiện liên quan.
- Tra cứu lỗi theo triệu chứng, mã lỗi hoặc nhóm phương tiện.
- Kho linh kiện, thông tin tương thích và trạng thái giá.
- Danh mục dụng cụ sửa chữa.
- Bảng giá sửa chữa có lọc theo ô tô/xe máy.
- Thư viện kiến thức tổng quan về FI/EFI.

## 5. Dữ liệu và an toàn
- Dữ liệu xe, lỗi và dụng cụ hiện tại là dữ liệu mẫu để kiểm tra giao diện/chức năng, chưa phải cơ sở dữ liệu đầy đủ.
- Giá linh kiện và giá sửa chữa được để ở trạng thái “Chưa cập nhật” cho đến khi có báo giá xác minh. Khi thêm giá, nên lưu đơn vị tiền, khu vực, ngày khảo sát, nguồn và điều kiện áp dụng.
- Không dùng phần tra cứu lỗi để tự kết luận hỏng hóc. Luôn đối chiếu tài liệu sửa chữa đúng phiên bản xe; công việc liên quan nhiên liệu áp suất cao, phanh, túi khí và điện áp cao cần người có chuyên môn.
- Website hiện chỉ cung cấp chức năng tra cứu; chưa có chức năng để khách truy cập thêm hoặc sửa dữ liệu.
- Khóa Flask lấy từ biến môi trường `SECRET_KEY`. Khi chạy local, app dùng khóa mặc định chỉ dành cho phát triển; không dùng khóa này trong production.

## 6. Đưa website lên Render
1. Đẩy thư mục dự án lên một repository GitHub.
2. Tạo tài khoản Render, chọn **New → Blueprint**, rồi kết nối repository đó.
3. Chọn file `render.yaml` trong thư mục `garage_library` và triển khai dịch vụ `motorlab`.
4. Sau khi deploy hoàn tất, mở URL `.onrender.com` do Render cung cấp để truy cập website.

Render tạo `SECRET_KEY` tự động và chạy ứng dụng bằng Gunicorn. Cơ sở dữ liệu SQLite được khởi tạo tự động với dữ liệu mẫu. Trên gói miễn phí, filesystem của dịch vụ không bền vững; dữ liệu tùy chỉnh có thể mất khi dịch vụ được tạo lại. Nếu cần quản lý nội dung lâu dài, hãy chuyển sang cơ sở dữ liệu lưu trữ bền vững trước khi bổ sung chức năng chỉnh sửa dữ liệu.

## 7. Khởi tạo lại dữ liệu mẫu
Cơ sở dữ liệu sẽ được tạo tự động khi chạy `python app.py`. Nếu muốn tạo lại toàn bộ dữ liệu mẫu từ đầu, hãy dừng ứng dụng và xóa file `instance/garage_library.db`, sau đó chạy lại. Thao tác này sẽ xóa mọi dữ liệu bạn đã tự thêm vào cơ sở dữ liệu.
