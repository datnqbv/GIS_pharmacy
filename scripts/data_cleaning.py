"""
Người 1 - Dữ liệu & Tiền xử lý
Làm sạch dữ liệu export.geojson và tạo file clean_pharmacy.geojson
"""

import json
import re
from pathlib import Path

# Đường dẫn file
INPUT_FILE = Path(__file__).parent.parent / "data" / "export.geojson"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "clean_pharmacy.geojson"

# Danh sách quận/huyện Hà Nội chuẩn
DISTRICT_MAPPING = {
    # Quận nội thành
    "ba đình": "Ba Đình",
    "ba dinh": "Ba Đình",
    "hoàn kiếm": "Hoàn Kiếm",
    "hoan kiem": "Hoàn Kiếm",
    "hai bà trưng": "Hai Bà Trưng",
    "hai ba trung": "Hai Bà Trưng",
    "đống đa": "Đống Đa",
    "dong da": "Đống Đa",
    "tây hồ": "Tây Hồ",
    "tay ho": "Tây Hồ",
    "cầu giấy": "Cầu Giấy",
    "cau giay": "Cầu Giấy",
    "thanh xuân": "Thanh Xuân",
    "thanh xuan": "Thanh Xuân",
    "hoàng mai": "Hoàng Mai",
    "hoang mai": "Hoàng Mai",
    "long biên": "Long Biên",
    "long bien": "Long Biên",
    "bắc từ liêm": "Bắc Từ Liêm",
    "bac tu liem": "Bắc Từ Liêm",
    "nam từ liêm": "Nam Từ Liêm",
    "nam tu liem": "Nam Từ Liêm",
    "hà đông": "Hà Đông",
    "ha dong": "Hà Đông",
    
    # Huyện ngoại thành
    "sóc sơn": "Sóc Sơn",
    "soc son": "Sóc Sơn",
    "đông anh": "Đông Anh",
    "dong anh": "Đông Anh",
    "gia lâm": "Gia Lâm",
    "gia lam": "Gia Lâm",
    "thanh trì": "Thanh Trì",
    "thanh tri": "Thanh Trì",
    "thường tín": "Thường Tín",
    "thuong tin": "Thường Tín",
    "hoài đức": "Hoài Đức",
    "hoai duc": "Hoài Đức",
    "đan phượng": "Đan Phượng",
    "dan phuong": "Đan Phượng",
    "mê linh": "Mê Linh",
    "me linh": "Mê Linh",
    "phúc thọ": "Phúc Thọ",
    "phuc tho": "Phúc Thọ",
    "thạch thất": "Thạch Thất",
    "thach that": "Thạch Thất",
    "quốc oai": "Quốc Oai",
    "quoc oai": "Quốc Oai",
    "chương mỹ": "Chương Mỹ",
    "chuong my": "Chương Mỹ",
    "thanh oai": "Thanh Oai",
    "mỹ đức": "Mỹ Đức",
    "my duc": "Mỹ Đức",
    "ứng hòa": "Ứng Hòa",
    "ung hoa": "Ứng Hòa",
    "phú xuyên": "Phú Xuyên",
    "phu xuyen": "Phú Xuyên",
    
    # Thị xã
    "sơn tây": "Sơn Tây",
    "son tay": "Sơn Tây",
}


def normalize_district(district_name):
    """Chuẩn hóa tên quận/huyện"""
    if not district_name or not isinstance(district_name, str):
        return None
    
    # Chuyển về chữ thường và loại bỏ khoảng trắng thừa
    district_lower = district_name.strip().lower()
    
    # Loại bỏ các tiền tố
    district_lower = re.sub(r'^(quận|huyện|thị xã)\s+', '', district_lower)
    
    # Tra cứu trong mapping
    return DISTRICT_MAPPING.get(district_lower, None)


def is_pharmacy(properties):
    """Kiểm tra xem có phải hiệu thuốc không"""
    amenity = properties.get("amenity", "")
    shop = properties.get("shop", "")
    
    return amenity == "pharmacy" or shop == "chemist"


def extract_pharmacy_info(feature):
    """Trích xuất thông tin cần thiết của hiệu thuốc"""
    props = feature.get("properties", {})
    geometry = feature.get("geometry", {})
    
    # Lấy tên hiệu thuốc
    name = props.get("name", props.get("brand", "Không rõ tên"))
    
    # Lấy địa chỉ
    addr_district = props.get("addr:district", "")
    addr_street = props.get("addr:street", "")
    addr_housenumber = props.get("addr:housenumber", "")
    
    # Chuẩn hóa quận
    normalized_district = normalize_district(addr_district)
    
    # Lấy giờ mở cửa
    opening_hours = props.get("opening_hours", "")
    
    # Lấy tọa độ
    coordinates = geometry.get("coordinates", [])
    
    # Lấy thêm một số thông tin khác
    phone = props.get("phone", props.get("contact:phone", ""))
    website = props.get("website", props.get("contact:website", ""))
    
    return {
        "type": "Feature",
        "properties": {
            "name": name,
            "district": normalized_district,
            "district_raw": addr_district,  # Giữ lại tên gốc để kiểm tra
            "street": addr_street,
            "housenumber": addr_housenumber,
            "opening_hours": opening_hours,
            "phone": phone,
            "website": website,
        },
        "geometry": geometry
    }


def clean_pharmacy_data():
    """Hàm chính để làm sạch dữ liệu"""
    print("🔄 Đang đọc file dữ liệu gốc...")
    
    # Đọc file GeoJSON
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Tổng số features: {len(data['features'])}")
    
    # Lọc và làm sạch dữ liệu
    clean_pharmacies = []
    pharmacy_count = 0
    has_district_count = 0
    
    for feature in data['features']:
        if is_pharmacy(feature.get('properties', {})):
            pharmacy_count += 1
            clean_feature = extract_pharmacy_info(feature)
            
            # Chỉ giữ lại các hiệu thuốc có quận hợp lệ
            if clean_feature['properties']['district']:
                has_district_count += 1
                clean_pharmacies.append(clean_feature)
    
    print(f"✅ Số hiệu thuốc tìm thấy: {pharmacy_count}")
    print(f"✅ Số hiệu thuốc có thông tin quận hợp lệ: {has_district_count}")
    
    # Thống kê các quận
    district_count = {}
    for pharmacy in clean_pharmacies:
        district = pharmacy['properties']['district']
        district_count[district] = district_count.get(district, 0) + 1
    
    print("\n📊 Thống kê theo quận/huyện:")
    for district in sorted(district_count.keys()):
        print(f"   {district}: {district_count[district]} hiệu thuốc")
    
    # Tạo GeoJSON mới
    clean_geojson = {
        "type": "FeatureCollection",
        "features": clean_pharmacies
    }
    
    # Lưu file
    print(f"\n💾 Đang lưu file clean_pharmacy.geojson...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(clean_geojson, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Hoàn thành! File đã được lưu tại: {OUTPUT_FILE}")
    print(f"📈 Tổng số hiệu thuốc sau khi làm sạch: {len(clean_pharmacies)}")


if __name__ == "__main__":
    clean_pharmacy_data()
