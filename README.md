#  Phân tích, thống kê và xây dựng bản đồ số hệ thống hiệu thuốc tại Hà Nội

Đề tài phân tích và trực quan hóa dữ liệu hiệu thuốc tại Hà Nội sử dụng dữ liệu OpenStreetMap.

##  Mô tả dự án

Dự án này thực hiện phân tích và trực quan hóa hệ thống hiệu thuốc tại Hà Nội, bao gồm:
- Làm sạch và chuẩn hóa dữ liệu
- Thống kê số lượng hiệu thuốc theo quận/huyện
- Vẽ các biểu đồ phân tích
- Xây dựng bản đồ tương tác

##  Cấu trúc dự án

```
GIS-Pharmacy-Hanoi/
│
├── data/
│   ├── export.geojson           # Dữ liệu gốc từ OpenStreetMap
│   └── clean_pharmacy.geojson   # Dữ liệu đã được làm sạch
│
├── scripts/
│   ├── data_cleaning.py        
│   ├── analysis.py             
│   └── map_visualization.py    
│
├── results/
│   ├── pharmacies_map.html      # Bản đồ tương tác
│   ├── chart_district.png       # Biểu đồ thống kê
│   └── pharmacy_by_district.csv # File CSV thống kê
│
├── requirements.txt             # Các thư viện cần thiết
└── README.md                    # File này
```

##  Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package manager)

### 2. Cài đặt thư viện

```bash
# Tạo môi trường ảo (khuyến nghị)
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

##  Chạy toàn bộ dự án

### Cách 1: Chạy từng script theo thứ tự

```bash
# Bước 1: Làm sạch dữ liệu
cd scripts
python data_cleaning.py

# Bước 2: Phân tích và thống kê
python analysis.py

# Bước 3: Tạo bản đồ
python map_visualization.py
```

### Cách 2: Chạy tất cả một lần

```bash
cd scripts
python data_cleaning.py && python analysis.py && python map_visualization.py
```

##  Kết quả mong đợi

### 1. Dữ liệu đã làm sạch
- File `data/clean_pharmacy.geojson` với dữ liệu chuẩn hóa
- Loại bỏ các bản ghi không có thông tin quận/huyện
- Chuẩn hóa tên quận theo danh sách chính thống

### 2. Thống kê
- File CSV với số lượng hiệu thuốc theo từng quận/huyện
- Biểu đồ cột, tròn, ngang thể hiện phân bố hiệu thuốc
- Thông tin quận có nhiều/ít hiệu thuốc nhất

### 3. Bản đồ tương tác
- Bản đồ HTML với tất cả hiệu thuốc
- Popup thông tin chi tiết khi click
- Layer control để lọc theo quận
- Layer control để lọc theo chuỗi hiệu thuốc
- MarkerCluster để hiển thị tốt hơn khi zoom out

##  Tính năng bản đồ

-  Hiển thị vị trí tất cả hiệu thuốc
-  Phân màu marker theo quận/huyện
- Popup với thông tin chi tiết (tên, địa chỉ, giờ mở cửa, SĐT)
- Layer control để bật/tắt hiển thị theo quận
-  Layer riêng cho các chuỗi lớn: Pharmacity, Long Châu, An Khang
-  MarkerCluster để nhóm các marker gần nhau
-  Tooltip hiển thị tên khi hover
-  Thống kê tổng quan hiển thị trên bản đồ
-  Nhiều kiểu bản đồ nền (OpenStreetMap, CartoDB)

##  Lưu ý

1. **Dữ liệu nguồn:** Dữ liệu được lấy từ OpenStreetMap, có thể không đầy đủ hoặc cập nhật
2. **Chuẩn hóa:** Script đã chuẩn hóa tên quận/huyện phổ biến, có thể cần bổ sung
3. **Font tiếng Việt:** Biểu đồ sử dụng DejaVu Sans, nếu không hiển thị đúng tiếng Việt, cài thêm font
4. **Bản đồ:** File HTML có thể nặng nếu có quá nhiều hiệu thuốc

##  Tùy chỉnh

### Thêm quận/huyện mới
Chỉnh sửa `DISTRICT_MAPPING` trong `scripts/data_cleaning.py`

### Đổi màu sắc quận
Chỉnh sửa `DISTRICT_COLORS` trong `scripts/map_visualization.py`

### Thêm chuỗi hiệu thuốc
Chỉnh sửa logic trong hàm `create_map()` của `scripts/map_visualization.py`

##  Công nghệ sử dụng

- **Python 3.x**: Ngôn ngữ lập trình chính
- **Pandas**: Xử lý và phân tích dữ liệu
- **Matplotlib**: Vẽ biểu đồ thống kê
- **Folium**: Tạo bản đồ tương tác (dựa trên Leaflet.js)
- **JSON**: Xử lý dữ liệu GeoJSON




