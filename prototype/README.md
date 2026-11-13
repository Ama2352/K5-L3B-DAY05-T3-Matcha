# Chạy prototype có AI

Cần Python 3 và file `.env` tại thư mục bài nộp, chứa `OPENAI_API_KEY=...`. Có thể đặt `OPENAI_MODEL=gpt-4.1-mini` (mặc định). Không commit `.env`.

Trong PowerShell tại thư mục bài nộp:

```powershell
python prototype/server.py
```

Trên macOS (Python cài từ python.org báo `CERTIFICATE_VERIFY_FAILED`):

```bash
SSL_CERT_FILE=$(python3 -m certifi) python3 prototype/server.py
```

Mở http://127.0.0.1:8766, nhập tình huống chỉ gồm dữ liệu giả, nhấn **Gửi cho AI**. AI phân loại yêu cầu; ứng dụng xử lý bằng các bước có sẵn và không cho AI trực tiếp đổi chuyến. Khi demo điểm thưởng, lưu ảnh màn hình thể hiện nhãn “AI đã phân loại” sau lời gọi thành công. Không chia sẻ API key.

Đây là máy chủ demo cục bộ, không triển khai ra Internet. Nếu API lỗi, ứng dụng hiển thị lỗi và không thực hiện thao tác; các nút mô phỏng vẫn dùng được.