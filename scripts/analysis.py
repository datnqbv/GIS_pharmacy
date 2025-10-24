"""
Người 2 - Phân tích & Thống kê
Đếm số lượng hiệu thuốc theo quận/huyện và vẽ biểu đồ
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from collections import Counter

# Thiết lập font hỗ trợ tiếng Việt
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Đường dẫn file
DATA_FILE = Path(__file__).parent.parent / "data" / "clean_pharmacy.geojson"
OUTPUT_CSV = Path(__file__).parent.parent / "results" / "pharmacy_by_district.csv"
OUTPUT_CHART = Path(__file__).parent.parent / "results" / "chart_district.png"


def load_pharmacy_data():
    """Đọc dữ liệu từ file clean_pharmacy.geojson"""
    print("🔄 Đang đọc dữ liệu hiệu thuốc...")
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pharmacies = []
    for feature in data['features']:
        props = feature['properties']
        pharmacies.append({
            'name': props.get('name', 'Không rõ tên'),
            'district': props.get('district'),
            'street': props.get('street', ''),
            'opening_hours': props.get('opening_hours', ''),
            'coordinates': feature['geometry']['coordinates']
        })
    
    return pd.DataFrame(pharmacies)


def analyze_by_district(df):
    """Phân tích số lượng hiệu thuốc theo quận/huyện"""
    print("\n📊 Đang thống kê theo quận/huyện...")
    
    # Đếm số lượng theo quận
    district_counts = df['district'].value_counts()
    
    # Tạo DataFrame để lưu
    analysis_df = pd.DataFrame({
        'Quận/Huyện': district_counts.index,
        'Số lượng hiệu thuốc': district_counts.values,
        'Tỷ lệ (%)': (district_counts.values / district_counts.sum() * 100).round(2)
    })
    
    # Lưu ra CSV
    analysis_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"✅ Đã lưu file CSV: {OUTPUT_CSV}")
    
    # In ra thống kê
    print("\n" + "="*60)
    print("THỐNG KÊ HIỆU THUỐC THEO QUẬN/HUYỆN")
    print("="*60)
    print(analysis_df.to_string(index=False))
    
    # Tìm quận có nhiều/ít nhất
    max_district = district_counts.idxmax()
    max_count = district_counts.max()
    min_district = district_counts.idxmin()
    min_count = district_counts.min()
    
    print("\n" + "="*60)
    print("PHÂN TÍCH")
    print("="*60)
    print(f"🏆 Quận có NHIỀU hiệu thuốc nhất: {max_district} ({max_count} hiệu thuốc)")
    print(f"📉 Quận có ÍT hiệu thuốc nhất: {min_district} ({min_count} hiệu thuốc)")
    print(f"📊 Tổng số hiệu thuốc: {district_counts.sum()}")
    print(f"📍 Số quận/huyện có hiệu thuốc: {len(district_counts)}")
    print(f"📈 Trung bình: {district_counts.mean():.1f} hiệu thuốc/quận")
    
    return analysis_df


def plot_charts(analysis_df):
    """Vẽ các biểu đồ thống kê"""
    print("\n🎨 Đang vẽ biểu đồ...")
    
    # Sắp xếp dữ liệu theo số lượng giảm dần
    sorted_df = analysis_df.sort_values('Số lượng hiệu thuốc', ascending=False)
    
    # Đường dẫn cho các biểu đồ riêng
    output_dir = Path(__file__).parent.parent / "results"
    chart_bar = output_dir / "chart_bar.png"
    chart_pie = output_dir / "chart_pie.png"
    chart_horizontal = output_dir / "chart_horizontal.png"
    
    # 1. Biểu đồ cột (riêng)
    print("  📊 Đang vẽ biểu đồ cột...")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    bars = ax1.bar(range(len(sorted_df)), sorted_df['Số lượng hiệu thuốc'], 
                   color='steelblue', alpha=0.8, edgecolor='navy')
    ax1.set_xlabel('Quận/Huyện', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Số lượng hiệu thuốc', fontsize=12, fontweight='bold')
    ax1.set_title('Biểu đồ cột: Số lượng hiệu thuốc theo quận/huyện', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.set_xticks(range(len(sorted_df)))
    ax1.set_xticklabels(sorted_df['Quận/Huyện'], rotation=45, ha='right', fontsize=10)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Thêm giá trị lên đỉnh cột
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(chart_bar, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ Đã lưu: {chart_bar.name}")
    
    # 2. Biểu đồ tròn (riêng)
    print("  🍰 Đang vẽ biểu đồ tròn...")
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    top_n = 10
    if len(sorted_df) > top_n:
        top_districts = sorted_df.head(top_n)
        others_sum = sorted_df.iloc[top_n:]['Số lượng hiệu thuốc'].sum()
        
        pie_labels = list(top_districts['Quận/Huyện']) + ['Các quận khác']
        pie_values = list(top_districts['Số lượng hiệu thuốc']) + [others_sum]
    else:
        pie_labels = list(sorted_df['Quận/Huyện'])
        pie_values = list(sorted_df['Số lượng hiệu thuốc'])
    
    colors = plt.cm.Set3(range(len(pie_values)))
    wedges, texts, autotexts = ax2.pie(pie_values, labels=pie_labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors,
                                        textprops={'fontsize': 11})
    ax2.set_title('Biểu đồ tròn: Tỷ lệ phân bố hiệu thuốc', 
                  fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(chart_pie, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ Đã lưu: {chart_pie.name}")
    
    # 3. Biểu đồ ngang (riêng)
    print("  📊 Đang vẽ biểu đồ ngang...")
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    top_15 = sorted_df.head(15)
    y_pos = range(len(top_15))
    bars = ax3.barh(y_pos, top_15['Số lượng hiệu thuốc'], 
                    color='coral', alpha=0.8, edgecolor='darkred')
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(top_15['Quận/Huyện'], fontsize=11)
    ax3.set_xlabel('Số lượng hiệu thuốc', fontsize=12, fontweight='bold')
    ax3.set_title('Top 15 quận/huyện có nhiều hiệu thuốc nhất', 
                  fontsize=14, fontweight='bold', pad=20)
    ax3.invert_yaxis()
    ax3.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Thêm giá trị
    for i, v in enumerate(top_15['Số lượng hiệu thuốc']):
        ax3.text(v + 0.1, i, str(int(v)), va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(chart_horizontal, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ Đã lưu: {chart_horizontal.name}")
    
    # Vẽ biểu đồ tổng hợp (giữ lại file gốc)
    print("  📊 Đang vẽ biểu đồ tổng hợp...")
    fig = plt.figure(figsize=(18, 6))
    
    # Subplot 1: Biểu đồ cột
    ax1 = plt.subplot(1, 3, 1)
    bars = ax1.bar(range(len(sorted_df)), sorted_df['Số lượng hiệu thuốc'], 
                   color='steelblue', alpha=0.8, edgecolor='navy')
    ax1.set_xlabel('Quận/Huyện', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Số lượng hiệu thuốc', fontsize=11, fontweight='bold')
    ax1.set_title('Biểu đồ cột: Số lượng hiệu thuốc theo quận/huyện', 
                  fontsize=12, fontweight='bold', pad=15)
    ax1.set_xticks(range(len(sorted_df)))
    ax1.set_xticklabels(sorted_df['Quận/Huyện'], rotation=45, ha='right', fontsize=9)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                ha='center', va='bottom', fontsize=8)
    
    # Subplot 2: Biểu đồ tròn
    ax2 = plt.subplot(1, 3, 2)
    wedges, texts, autotexts = ax2.pie(pie_values, labels=pie_labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors,
                                        textprops={'fontsize': 9})
    ax2.set_title('Biểu đồ tròn: Tỷ lệ phân bố hiệu thuốc', 
                  fontsize=12, fontweight='bold', pad=15)
    
    # Subplot 3: Biểu đồ ngang
    ax3 = plt.subplot(1, 3, 3)
    ax3.barh(y_pos, top_15['Số lượng hiệu thuốc'], 
             color='coral', alpha=0.8, edgecolor='darkred')
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(top_15['Quận/Huyện'], fontsize=9)
    ax3.set_xlabel('Số lượng hiệu thuốc', fontsize=11, fontweight='bold')
    ax3.set_title('Top 15 quận/huyện có nhiều hiệu thuốc nhất', 
                  fontsize=12, fontweight='bold', pad=15)
    ax3.invert_yaxis()
    ax3.grid(axis='x', alpha=0.3, linestyle='--')
    for i, v in enumerate(top_15['Số lượng hiệu thuốc']):
        ax3.text(v + 1, i, str(int(v)), va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_CHART, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✅ Đã lưu biểu đồ tổng hợp: {OUTPUT_CHART.name}")
    
    print("\n🎉 Hoàn thành! Đã tạo 4 file biểu đồ:")
    print(f"   1. {chart_bar.name} - Biểu đồ cột")
    print(f"   2. {chart_pie.name} - Biểu đồ tròn")
    print(f"   3. {chart_horizontal.name} - Biểu đồ ngang")
    print(f"   4. {OUTPUT_CHART.name} - Biểu đồ tổng hợp")


def main():
    """Hàm chính"""
    print("="*60)
    print("PHÂN TÍCH & THỐNG KÊ HIỆU THUỐC HÀ NỘI")
    print("="*60)
    
    # Đọc dữ liệu
    df = load_pharmacy_data()
    
    # Phân tích theo quận
    analysis_df = analyze_by_district(df)
    
    # Vẽ biểu đồ
    plot_charts(analysis_df)
    
    print("\n✅ Hoàn thành phân tích!")


if __name__ == "__main__":
    main()
