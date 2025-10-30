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
│   ├── data_cleaning.py        # Làm sạch dữ liệu hiệu thuốc
│   ├── analysis.py             # Thống kê, xuất biểu đồ, CSV
│   ├── map_visualization.py    # Tạo bản đồ tương tác
│   └── pharmacy_buffer_analysis.py # Phân tích hiệu thuốc trong bán kính, vẽ buffer
│
├── results/
│   ├── pharmacies_map.html      # Bản đồ tương tác tổng thể
│   ├── chart_district.png       # Biểu đồ thống kê
│   ├── pharmacies_buffer_map.html # Bản đồ hiệu thuốc trong bán kính
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

# (Tùy chọn nâng cao) Phân tích hiệu thuốc trong bán kính X mét quanh một điểm:
python pharmacy_buffer_analysis.py
```


### Cách 2: Chạy tất cả một lần (không bao gồm buffer analysis)

```bash
cd scripts
python data_cleaning.py && python analysis.py && python map_visualization.py
```

##  Phân chia công việc nhóm

Dự án phù hợp cho nhóm 3 người, mỗi người phụ trách một mảng chính:

1. **Làm sạch dữ liệu** (data_cleaning.py): Chuẩn hóa, loại bỏ bản ghi lỗi, chuẩn hóa tên quận/huyện, xuất GeoJSON sạch.
2. **Phân tích & Thống kê** (analysis.py): Thống kê số lượng hiệu thuốc theo quận, xuất CSV, vẽ biểu đồ.
3. **Bản đồ & Trực quan hóa** (map_visualization.py, pharmacy_buffer_analysis.py): Tạo bản đồ tổng thể, bản đồ buffer, thêm các tính năng tìm kiếm, phân cụm, popup, v.v.

##  Tính năng nâng cao

- **Tìm kiếm hiện đại trên bản đồ**: Tìm hiệu thuốc theo tên, tự động gợi ý, zoom và highlight.
- **Phân tích buffer (bán kính)**: Tìm và trực quan hóa các hiệu thuốc nằm trong bán kính X mét quanh một điểm bất kỳ (ví dụ quanh Bệnh viện Bạch Mai), sử dụng công thức Haversine.
- **Vẽ buffer trên bản đồ**: Vòng tròn bán kính, marker trung tâm, phân biệt hiệu thuốc trong/ngoài vùng buffer.

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


##  Công nghệ & thư viện sử dụng

- **Python 3.x**: Ngôn ngữ lập trình chính
- **Pandas**: Xử lý và phân tích dữ liệu
- **Matplotlib**: Vẽ biểu đồ thống kê
- **Folium**: Tạo bản đồ tương tác (dựa trên Leaflet.js)
- **JSON**: Xử lý dữ liệu GeoJSON
- **math**: Tính toán khoảng cách (Haversine)
- **requests**: (nếu dùng geocoding tự động)
# ---
#
# **Tóm tắt quy trình thực hiện dự án:**
#
# 1. Thu thập dữ liệu hiệu thuốc từ OpenStreetMap (file export.geojson)
# 2. Làm sạch và chuẩn hóa dữ liệu (data_cleaning.py)
# 3. Thống kê, xuất biểu đồ, CSV (analysis.py)
# 4. Tạo bản đồ tương tác tổng thể (map_visualization.py)
# 5. (Nâng cao) Phân tích và trực quan hóa hiệu thuốc trong bán kính (pharmacy_buffer_analysis.py)
#
# **Kết quả:**
# - Dữ liệu sạch, thống kê chi tiết, bản đồ HTML tương tác, bản đồ buffer, biểu đồ, CSV.
#
# **Phù hợp cho báo cáo, thuyết trình, hoặc nộp bài tập môn GIS.**




