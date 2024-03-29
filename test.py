import pandas as pd
import re
from unidecode import unidecode

# Đọc dữ liệu từ tập tin Excel
df = pd.read_excel("Vung-Khuvuc.xlsx")

# Loại bỏ khoảng trắng ở cuối mỗi giá trị trong cột "Huyện, Tỉnh"
df["Huyện, Tỉnh"] = df["Huyện, Tỉnh"].str.strip()

# Đọc dữ liệu từ tệp văn bản "Vung.txt"
with open('Vung.txt', 'r', encoding='utf-16') as f:
    vung_data = f.read()
vung_data = vung_data.replace("-", ",")

# Tạo một danh sách chứa tên vùng và tỉnh thành từ file Vung.txt
regions_mapping = {}
for match in re.finditer(r"Vùng\s([^:]+)\s.*?gồm\s(\d+\s)?tỉnh(?: thành)?:\s(.*?)\.", vung_data):
    region_name = match.group(1).strip()  # Lấy tên vùng từ nhóm ký tự không phải khoảng trắng
    provinces_str = match.group(3).strip()  # Lấy chuỗi các tỉnh
    # Xử lý trường hợp đặc biệt khi có từ "và" trong chuỗi tỉnh
    provinces = [province.strip().lower() for province in re.split(r',|và', provinces_str) if province.strip()]
    regions_mapping.update({province: region_name for province in provinces})

# Đọc dữ liệu từ tệp văn bản "TayBac.txt"
with open('TayBac.txt', 'r', encoding='utf-16') as f:
    taybac_data = f.read()
# Tạo danh sách các huyện và tỉnh thuộc khu vực nông thôn và thành thị
districts_rural = re.findall(r'Huyện\s(.+?)\s\(.+?\)', taybac_data)
districts_urban = re.findall(r'(Thành phố\s.+?)\s\(.+?\)', taybac_data)

def check_district_area(district_name, region):
    if pd.isna(district_name) or region != "Tây Bắc Bộ":  # Kiểm tra xem giá trị là NaN hoặc "Vùng" không phải là "Tây Bắc Bộ"
        return None
    normalized_name = unidecode(str(district_name)).lower()  # Chuẩn hóa tên huyện
    # Kiểm tra xem có huyện nào trong danh sách "Khu vực nông thôn" có chứa phần của chuỗi không
    for rural_district in districts_rural:
        if unidecode(rural_district.lower()) in normalized_name:
            return "Nông Thôn"
    # Kiểm tra xem có huyện nào trong danh sách "Khu vực thành thị" có chứa phần của chuỗi không
    for urban_district in districts_urban:
        if unidecode(urban_district.lower()) in normalized_name:
            return "Thành Thị"
    return None

# Hàm để kiểm tra tên tỉnh và trả về tên vùng tương ứng
def check_province_name(province_name):
    if isinstance(province_name, str):  # Kiểm tra nếu là một chuỗi
        # Kiểm tra xem chuỗi có chứa bất kỳ tỉnh thành nào trong danh sách không
        for province, region in regions_mapping.items():
            # Giữ nguyên chuỗi tỉnh thành, chỉ loại bỏ khoảng trắng ở đầu và cuối
            province_normalized = unidecode(province).strip()
            province_name_normalized = unidecode(province_name).strip()
            # Tạo một biểu thức chính quy để tìm kiếm toàn bộ tên tỉnh thành trong chuỗi
            pattern = r"\b{}\b".format(province_normalized)
            if re.search(pattern, province_name_normalized.lower(), re.IGNORECASE):
                return region
            if "BRVT" in province_name_normalized.upper():
                return "Đông Nam Bộ"
            if "HCM" in province_name_normalized.upper():
                return "Đông Nam Bộ"
    return None

# Tạo cột "Vùng" dựa trên thông tin từ file "Vung.txt"
df["Vùng"] = df["Huyện, Tỉnh"].map(check_province_name)

# Tạo cột "Khu vực" dựa trên thông tin từ file "TayBac.txt"
df["Khu vực"] = df.apply(lambda row: check_district_area(row["Huyện, Tỉnh"], row["Vùng"]), axis=1)

# Lưu dữ liệu vào tệp Excel mới
# df.to_excel("updated_Vung-Khuvuc.xlsx", index=False)
