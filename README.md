# Safety Helmet Vision App

Ứng dụng phát hiện mũ bảo hộ lao động theo thời gian thực sử dụng YOLOv8 và Streamlit.

---

## Giới thiệu

Ứng dụng cho phép người dùng tải lên hình ảnh hoặc video và tự động phát hiện xem người trong khung hình có đội mũ bảo hộ hay không. Mô hình được huấn luyện dựa trên YOLOv8s và chạy trực tiếp trên trình duyệt thông qua Streamlit Cloud (CPU).

---

## Tính năng

- Phát hiện mũ bảo hộ trên **ảnh tĩnh** (JPG, PNG)
- Phát hiện mũ bảo hộ trên **video** (MP4, AVI, MOV)
- Điều chỉnh tốc độ xử lý video qua thanh trượt **Frame Skip**
- Tái sử dụng kết quả khung hình trước để tránh nhấp nháy khi bỏ qua frame
- Triển khai sẵn sàng trên **Streamlit Cloud**

---

## Cách sử dụng

### 1. Chạy cục bộ

```bash
# Clone repository
git clone https://github.com/khoithetran/Safety-helmet-vision-app.git
cd Safety-helmet-vision-app

# Cài đặt các thư viện
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

### 2. Truy cập trên Streamlit Cloud

Mở ứng dụng đã triển khai tại Streamlit Cloud, chọn chế độ **Image** hoặc **Video**, sau đó tải file lên.

---

## Cấu trúc dự án

```
Safety-helmet-vision-app/
├── app.py                  # Ứng dụng Streamlit chính
├── models/
│   └── yolov8s_ap.pt       # Trọng số mô hình YOLOv8 đã huấn luyện
├── requirements.txt        # Danh sách thư viện Python
└── README.md
```

---

## Tối ưu hiệu suất (Frame Skipping)

Do Streamlit Cloud chạy trên CPU, tốc độ suy luận mô hình có thể chậm. Tính năng **Frame Skip** giúp tăng tốc độ xử lý:

| Giá trị Frame Skip | Ý nghĩa |
|---|---|
| `1` | Chạy mô hình trên mỗi frame (chậm nhất, chính xác nhất) |
| `3` *(mặc định)* | Chạy mô hình 1 trong 3 frame — cân bằng tốt |
| `5–10` | Xử lý nhanh nhất, bounding box cập nhật ít thường xuyên hơn |

Các frame bị bỏ qua sẽ tái sử dụng kết quả từ lần dự đoán gần nhất để hiển thị liên tục, không bị nhấp nháy.

---

## Công nghệ sử dụng

- [YOLOv8 (Ultralytics)](https://github.com/ultralytics/ultralytics) — mô hình phát hiện đối tượng
- [Streamlit](https://streamlit.io/) — giao diện web
- [OpenCV](https://opencv.org/) — xử lý video
- [PyTorch](https://pytorch.org/) — framework deep learning

---

## Tác giả

**Khoi Tran**
