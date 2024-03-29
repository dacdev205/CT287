# Hướng dẫn cập nhật thông tin vùng khu vực

## Giới thiệu
Tệp này cung cấp hướng dẫn và mã nguồn để cập nhật thông tin về vùng khu vực dựa trên dữ liệu từ tệp Excel và văn bản.

## Yêu cầu
- Python 3.x
- Thư viện pandas
- Thư viện unidecode

## Cách sử dụng
1. Đảm bảo bạn đã cài đặt Python và các thư viện cần thiết (pandas, unidecode).
2. Đưa dữ liệu về vùng khu vực vào tệp `Vung.txt` theo định dạng như sau:
   - Mỗi dòng mô tả một vùng khu vực.
   - Mỗi dòng bao gồm tên vùng, số lượng tỉnh và danh sách các tỉnh thành của vùng đó.
   - Dùng dấu ":" để phân tách tên vùng và danh sách tỉnh thành.
   - Dùng dấu ",", "-" hoặc "và" để phân tách các tỉnh thành trong danh sách.
3. Chạy mã nguồn Python để cập nhật thông tin vùng khu vực:
   ```bash
   python test.py
