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
    
    # Danh sách marker cho Search
    search_markers = []
    
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
        marker = folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=name,
            icon=folium.Icon(color=color, icon='plus-sign', prefix='glyphicon')
        )
        marker.add_to(marker_cluster)
        search_markers.append({'marker': marker, 'name': name, 'address': address})
        
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
    
    # Thêm chức năng tìm kiếm hiện đại với autocomplete và zoom
    search_data = []
    for pharmacy in pharmacies:
        props = pharmacy['properties']
        coords = pharmacy['geometry']['coordinates']
        search_data.append({
            'name': props.get('name', 'Không rõ'),
            'district': props.get('district', 'Không rõ'),
            'street': props.get('street', ''),
            'phone': props.get('phone', 'Không có'),
            'hours': props.get('opening_hours', 'Không có thông tin'),
            'lat': coords[1],
            'lon': coords[0]
        })
    
    # Tạo JavaScript cho tìm kiếm hiện đại
    search_js = f"""
    <script>
    var pharmaciesData = {json.dumps(search_data, ensure_ascii=False)};
    
    // Đợi DOM load xong
    document.addEventListener('DOMContentLoaded', function() {{
        // Tạo search box hiện đại
        var searchHTML = `
            <div id="modern-search" style="position: absolute; top: 10px; left: 50px; z-index: 1000;">
                <div style="background: white; padding: 15px 20px; border-radius: 25px; 
                            box-shadow: 0 4px 15px rgba(0,0,0,0.2); display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 20px;">🔍</span>
                    <input type="text" id="pharmacy-search" placeholder="Tìm hiệu thuốc theo tên hoặc địa chỉ..." 
                           style="border: none; outline: none; width: 350px; font-size: 14px; font-family: Arial;">
                    <button id="clear-search" style="background: none; border: none; cursor: pointer; 
                            font-size: 18px; color: #999; display: none;">✕</button>
                </div>
                <div id="search-results" style="position: absolute; top: 60px; left: 0; right: 0; 
                     background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); 
                     max-height: 400px; overflow-y: auto; display: none; z-index: 1001;"></div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', searchHTML);
        
        var searchInput = document.getElementById('pharmacy-search');
        var searchResults = document.getElementById('search-results');
        var clearBtn = document.getElementById('clear-search');
        
        // Tìm kiếm và hiển thị kết quả
        searchInput.addEventListener('input', function(e) {{
        var query = e.target.value.toLowerCase().trim();
        
        if (query.length === 0) {{
            searchResults.style.display = 'none';
            clearBtn.style.display = 'none';
            return;
        }}
        
        clearBtn.style.display = 'block';
        
        // Lọc kết quả
        var matches = pharmaciesData.filter(function(p) {{
            return p.name.toLowerCase().includes(query) || 
                   p.district.toLowerCase().includes(query) ||
                   p.street.toLowerCase().includes(query);
        }}).slice(0, 10); // Giới hạn 10 kết quả
        
        if (matches.length === 0) {{
            searchResults.innerHTML = '<div style="padding: 15px; color: #999; text-align: center;">Không tìm thấy kết quả</div>';
            searchResults.style.display = 'block';
            return;
        }}
        
        // Hiển thị kết quả
        var html = matches.map(function(p, index) {{
            var address = p.street ? p.street + ', ' + p.district : p.district;
            return `
                <div class="search-item" data-index="${{index}}" data-lat="${{p.lat}}" data-lon="${{p.lon}}"
                     style="padding: 12px 20px; border-bottom: 1px solid #f0f0f0; cursor: pointer; 
                            transition: background 0.2s;">
                    <div style="font-weight: bold; color: #1976D2; margin-bottom: 4px;">🏥 ${{p.name}}</div>
                    <div style="font-size: 12px; color: #666;">📍 ${{address}}</div>
                    <div style="font-size: 11px; color: #999; margin-top: 2px;">📞 ${{p.phone}} | 🕐 ${{p.hours}}</div>
                </div>
            `;
        }}).join('');
        
        searchResults.innerHTML = html;
        searchResults.style.display = 'block';
        
        // Thêm hover effect
        document.querySelectorAll('.search-item').forEach(function(item) {{
            item.addEventListener('mouseenter', function() {{
                this.style.background = '#f5f5f5';
            }});
            item.addEventListener('mouseleave', function() {{
                this.style.background = 'white';
            }});
            
            // Click để zoom
            item.addEventListener('click', function() {{
                var lat = parseFloat(this.dataset.lat);
                var lon = parseFloat(this.dataset.lon);
                
                // Zoom vào vị trí hiệu thuốc
                {m.get_name()}.setView([lat, lon], 17);
                
                // Ẩn kết quả tìm kiếm
                searchResults.style.display = 'none';
                searchInput.value = '';
                clearBtn.style.display = 'none';
                
                // Highlight marker (tùy chọn: có thể thêm hiệu ứng nhấp nháy)
                setTimeout(function() {{
                    // Tạo hiệu ứng pulse tại vị trí
                    var pulseCircle = L.circle([lat, lon], {{
                        color: '#ff0000',
                        fillColor: '#ff0000',
                        fillOpacity: 0.3,
                        radius: 100
                    }}).addTo({m.get_name()});
                    
                    // Xóa sau 2 giây
                    setTimeout(function() {{
                        {m.get_name()}.removeLayer(pulseCircle);
                    }}, 2000);
                }}, 300);
            }});
        }});
    }});
        
        // Nút clear
        clearBtn.addEventListener('click', function() {{
            searchInput.value = '';
            searchResults.style.display = 'none';
            clearBtn.style.display = 'none';
            searchInput.focus();
        }});
        
        // Ẩn kết quả khi click bên ngoài
        document.addEventListener('click', function(e) {{
            if (!document.getElementById('modern-search').contains(e.target)) {{
                searchResults.style.display = 'none';
            }}
        }});
    }});
    </script>
    """
    
    m.get_root().html.add_child(folium.Element(search_js))
    
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
