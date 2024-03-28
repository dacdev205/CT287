import pandas as pd
import re
from unidecode import unidecode

# Đọc dữ liệu từ tập tin Excel

df = pd.read_excel("Vung-Khuvuc.xlsx")

# Loại bỏ khoảng trắng ở cuối mỗi giá trị trong cột "Huyện, Tỉnh"
df["Huyện, Tỉnh"] = df["Huyện, Tỉnh"].str.strip()

# Đọc dữ liệu từ tệp văn bản
with open('Vung.txt', 'r', encoding='utf-16') as f:
    vung_data = f.read()

# Tạo một danh sách chứa tên vùng và tỉnh thành từ file Vung.txt
regions_mapping = {}
for match in re.finditer(r"Vùng\s([^:]+)\s.*?gồm\s(\d+\s)?tỉnh(?: thành)?:\s(.*?)\.", vung_data):
    region_name = match.group(1).strip()  # Lấy tên vùng từ nhóm ký tự không phải khoảng trắng
    provinces_str = match.group(3).strip()  # Lấy chuỗi các tỉnh
    # Xử lý trường hợp đặc biệt khi có từ "và" trong chuỗi tỉnh
    provinces = [province.strip().lower() for province in re.split(r',|và', provinces_str) if province.strip()]
    regions_mapping.update({province: region_name for province in provinces})

def check_province_name(province_name):
    if isinstance(province_name, str):  # Kiểm tra nếu là một chuỗi
        # Kiểm tra xem chuỗi có chứa bất kỳ tỉnh thành nào trong danh sách không
        for province, region in regions_mapping.items():
            # Chuyển đổi các ký tự có dấu thành ký tự không dấu trước khi so sánh
            province_normalized = unidecode(province)
            province_name_normalized = unidecode(province_name)
            # Tạo một biểu thức chính quy để tìm kiếm tên tỉnh thành trong chuỗi
            pattern = r"\b{}\b".format(province_normalized.replace(" ", r"[\s-]*"))
            if re.search(pattern, province_name_normalized.lower(), re.IGNORECASE):
                return region
            # Kiểm tra các từ có chữ cái đầu giống nhau trong tỉnh thành và trong danh sách
            if all(word.lower() in province_normalized.lower().split() for word in province_name.split()):
                return region
    return None

# Gán tên vùng cho từng tỉnh trong DataFrame
df["Vùng"] = df["Huyện, Tỉnh"].map(check_province_name)

# Lưu dữ liệu vào tệp Excel mới
df.to_excel("updated_Vung-Khuvuc.xlsx", index=False)
