"""
Tìm tất cả hiệu thuốc trong bán kính X mét quanh một điểm (lat, lon)
"""

import json
from pathlib import Path
from math import radians, cos, sin, asin, sqrt
import folium

# Công thức Haversine để tính khoảng cách giữa hai điểm vĩ độ/kinh độ (tính bằng mét)
def haversine(lon1, lat1, lon2, lat2):
    # chuyển đổi độ thập phân sang radian
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # công thức haversine
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000  # Bán kính của trái đất tính bằng mét
    return c * r

# Cấu hình
DATA_FILE = Path(__file__).parent.parent / "data" / "clean_pharmacy.geojson"


# Điểm trung tâm (ví dụ: Bệnh viện Bạch Mai)
CENTER_LAT = 21.0021
CENTER_LON = 105.8520
RADIUS_M = 1000  # bán kính (mét)

# File HTML kết quả
OUTPUT_MAP = Path(__file__).parent.parent / "results" / "pharmacies_buffer_map.html"

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

pharmacies = data['features']


# Tìm hiệu thuốc trong bán kính
in_radius = []
for pharmacy in pharmacies:
    coords = pharmacy['geometry']['coordinates']  # Lấy tọa độ (kinh độ, vĩ độ) của hiệu thuốc
    lon, lat = coords[0], coords[1] # Gán kinh độ cho lon, vĩ độ cho lat
    dist = haversine(CENTER_LON, CENTER_LAT, lon, lat)# Tính khoảng cách từ điểm trung tâm đến hiệu thuốc (đơn vị mét)
    if dist <= RADIUS_M: # Nếu khoảng cách nhỏ hơn hoặc bằng bán kính cho trước
        in_radius.append({ # Thêm hiệu thuốc vào danh sách in_radius với các thông tin:
            'name': pharmacy['properties'].get('name', 'Không rõ'), # Tên hiệu thuốc (nếu không có thì ghi 'Không rõ')
            'district': pharmacy['properties'].get('district', 'Không rõ'),
            'street': pharmacy['properties'].get('street', ''),
            'distance_m': round(dist, 1),
            'lat': lat, # Vĩ độ
            'lon': lon # Kinh độ
        })

print(f"Có {len(in_radius)} hiệu thuốc trong bán kính {RADIUS_M}m quanh điểm ({CENTER_LAT}, {CENTER_LON})")
for p in in_radius:
    print(f"- {p['name']} ({p['district']}, {p['street']}) - {p['distance_m']}m")

# Trực quan hóa trên bản đồ Folium
m = folium.Map(location=[CENTER_LAT, CENTER_LON], zoom_start=15, tiles='OpenStreetMap')

# Vẽ buffer (vòng tròn bán kính)
folium.Circle(
    location=[CENTER_LAT, CENTER_LON],
    radius=RADIUS_M,
    color='red',
    fill=True,
    fill_opacity=0.1,
    popup=f"Bán kính {RADIUS_M}m"
).add_to(m)

# Marker điểm trung tâm
folium.Marker(
    location=[CENTER_LAT, CENTER_LON],
    icon=folium.Icon(color='red', icon='star'),
    popup="Điểm trung tâm"
).add_to(m)

# Marker các hiệu thuốc trong bán kính (màu xanh đậm)
for p in in_radius:
    folium.Marker(
        location=[p['lat'], p['lon']],
        popup=f" {p['name']}<br> {p['street']}, {p['district']}<br> {p['distance_m']}m",
        icon=folium.Icon(color='blue', icon='plus-sign', prefix='glyphicon')
    ).add_to(m)

# Marker các hiệu thuốc ngoài bán kính (màu xám nhạt)
for pharmacy in pharmacies:
    coords = pharmacy['geometry']['coordinates']
    lon, lat = coords[0], coords[1]
    if not any(abs(lat-p['lat'])<1e-6 and abs(lon-p['lon'])<1e-6 for p in in_radius):
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color='gray',
            fill=True,
            fill_opacity=0.3,
            popup=pharmacy['properties'].get('name', 'Không rõ')
        ).add_to(m)

# Lưu bản đồ
m.save(str(OUTPUT_MAP))
print(f"\n Đã lưu bản đồ buffer: {OUTPUT_MAP}")
