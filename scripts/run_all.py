"""
Script tổng hợp - Chạy toàn bộ pipeline phân tích hiệu thuốc Hà Nội
Chạy file này để thực hiện tất cả các bước: làm sạch, phân tích, và tạo bản đồ
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Chạy một script Python"""
    print("\n" + "="*60)
    print(f" {description}")
    print("="*60)
    
    script_path = Path(__file__).parent / script_name
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        print(f" {description} - HOÀN THÀNH!")
        return True
    except subprocess.CalledProcessError as e:
        print(f" Lỗi khi chạy {script_name}: {e}")
        return False
    except Exception as e:
        print(f" Lỗi không xác định: {e}")
        return False


def main():
    """Hàm chính - chạy toàn bộ pipeline"""
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "   PHÂN TÍCH HỆ THỐNG HIỆU THUỐC HÀ NỘI  ".center(58) + "║")
    print("║" + "  Pipeline tự động - Chạy tất cả các bước  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Danh sách các bước
    steps = [
        ("data_cleaning.py", "Bước 1: Làm sạch và tiền xử lý dữ liệu"),
        ("analysis.py", "Bước 2: Phân tích và thống kê"),
        ("map_visualization.py", "Bước 3: Tạo bản đồ tương tác"),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    # Chạy từng bước
    for script_name, description in steps:
        if run_script(script_name, description):
            success_count += 1
        else:
            print(f"\n  Pipeline dừng tại: {description}")
            break
    
    # Tổng kết
    print("\n" + "="*60)
    print(" TỔNG KẾT")
    print("="*60)
    print(f" Hoàn thành: {success_count}/{total_steps} bước")
    
    if success_count == total_steps:
        print("\n Pipeline hoàn thành thành công!")
        print("\n Các file kết quả:")
        print("   • data/clean_pharmacy.geojson - Dữ liệu đã làm sạch")
        print("   • results/pharmacy_by_district.csv - Thống kê CSV")
        print("   • results/chart_district.png - Biểu đồ phân tích")
        print("   • results/pharmacies_map.html - Bản đồ tương tác")
        print("\n Mở file pharmacies_map.html để xem bản đồ!")
    else:
        print("\n Pipeline chưa hoàn thành. Vui lòng kiểm tra lỗi ở trên.")
        sys.exit(1)


if __name__ == "__main__":
    main()
