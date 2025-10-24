"""
Người 3 - Trực quan hóa bản đồ (Phiên bản đơn giản)
Hiển thị bản đồ hiệu thuốc bằng Folium
"""

import json
import folium
from folium.plugins import MarkerCluster
from pathlib import Path

# Cấu hình
DATA_FILE = Path(__file__).parent.parent / "data" / "clean_pharmacy.geojson"
OUTPUT_MAP = Path(__file__).parent.parent / "results" / "pharmacies_map.html"
HANOI_CENTER = [21.0285, 105.8542]

# Màu theo quận
COLORS = {
    'Bắc Từ Liêm': 'darkgreen', 'Đống Đa': 'purple', 'Hai Bà Trưng': 'green',
    'Cầu Giấy': 'darkred', 'Thanh Xuân': 'orange', 'Long Biên': 'darkblue',
    'Tây Hồ': 'lightblue', 'Hoàn Kiếm': 'blue', 'Ba Đình': 'red',
    'Hoàng Mai': 'beige', 'Nam Từ Liêm': 'cadetblue'
}


def create_map():
    """Tạo bản đồ hiệu thuốc"""
    print("🗺️  Đang tạo bản đồ...")
    
    # Đọc dữ liệu
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pharmacies = data['features']
    print(f"📍 Tìm thấy {len(pharmacies)} hiệu thuốc")
    
    # Tạo bản đồ
    m = folium.Map(location=HANOI_CENTER, zoom_start=11, tiles='OpenStreetMap')
    
    # Thêm tile layer khác
    folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
    
    # Tạo marker cluster
    marker_cluster = MarkerCluster(name='Tất cả hiệu thuốc').add_to(m)
    
    # Tạo feature group cho từng quận
    district_groups = {}
    
    # Thêm marker
    for pharmacy in pharmacies:
        props = pharmacy['properties']
        coords = pharmacy['geometry']['coordinates']
        lat, lon = coords[1], coords[0]
        
        # Thông tin
        name = props.get('name', 'Không rõ')
        district = props.get('district', 'Không rõ')
        street = props.get('street', '')
        hours = props.get('opening_hours', 'Không có thông tin')
        phone = props.get('phone', 'Không có')
        
        # Địa chỉ
        address = f"{street}, {district}" if street else district
        
        # Popup HTML đơn giản
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="color: #1976D2; margin: 0 0 10px 0;">🏥 {name}</h4>
            <p><b>📍 Địa chỉ:</b> {address}</p>
            <p><b>🏛️ Quận:</b> {district}</p>
            <p><b>🕐 Giờ mở:</b> {hours}</p>
            <p><b>📞 SĐT:</b> {phone}</p>
        </div>
        """
        
        # Màu sắc
        color = COLORS.get(district, 'gray')
        
        # Tạo feature group cho quận
        if district not in district_groups:
            district_groups[district] = folium.FeatureGroup(name=f'📍 {district}')
            district_groups[district].add_to(m)
        
        # Thêm vào cluster
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=name,
            icon=folium.Icon(color=color, icon='plus-sign', prefix='glyphicon')
        ).add_to(marker_cluster)
        
        # Thêm vào group quận
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=name,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7
        ).add_to(district_groups[district])
    
    # Layer control
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Thêm legend
    legend_html = f"""
    <div style="position: fixed; bottom: 50px; right: 50px; width: 200px;
                background-color: white; border: 2px solid #1976D2;
                border-radius: 5px; padding: 10px; z-index: 9999;">
        <h4 style="margin: 0 0 10px 0; color: #1976D2;">📊 Thống kê</h4>
        <p style="margin: 5px 0;"><b>Tổng:</b> {len(pharmacies)} hiệu thuốc</p>
        <p style="margin: 5px 0;"><b>Quận:</b> {len(district_groups)} quận</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Lưu
    m.save(str(OUTPUT_MAP))
    print(f"✅ Đã lưu: {OUTPUT_MAP}")


if __name__ == "__main__":
    print("="*60)
    print("TRỰC QUAN HÓA BẢN ĐỒ HIỆU THUỐC HÀ NỘI")
    print("="*60)
    create_map()
    print("\n✅ Hoàn thành!")
