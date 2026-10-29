# CEH v13 Extended Toolkit

Bộ công cụ tự động hóa thu thập thông tin và kiểm thử an ninh mạng (Reconnaissance, Scanning, Enumeration, Vulnerability Analysis & Web Hacking) theo chuẩn giáo trình CEH v13.

## Cấu trúc thư mục

```text
BT1 CEH/
├── main.py              # File chạy chính (CLI)
├── config.yaml          # File cấu hình quét
├── requirements.txt     # Danh sách thư viện Python cần thiết
├── core/                # Các thành phần lõi (logger, orchestrator, base module)
├── modules/             # Các module chức năng (m02, m03, m04, m05, m11, report)
└── output/              # Thư mục lưu báo cáo HTML và JSON
```

## Cài đặt

1. Tạo môi trường ảo:
```bash
python -m venv .venv
```

2. Kích hoạt môi trường ảo:
- Trên Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
- Trên Linux/macOS:
```bash
source .venv/bin/activate
```

3. Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

## Hướng dẫn sử dụng

### 1. Liệt kê các module có sẵn
```bash
python main.py list
```

### 2. Quét mục tiêu
- Quét đầy đủ các module theo file `config.yaml`:
```bash
python main.py scan <target_domain_hoac_ip>
```

- Quét với các module cụ thể:
```bash
python main.py scan 127.0.0.1 --modules m03_scanning,m04_enumeration
```

- Chạy tuần tự thay vì đa luồng:
```bash
python main.py scan example.com --no-parallel
```

### 3. Báo cáo kết quả
Sau khi quét xong, kết quả được xuất ra 2 tệp tại thư mục `./output`:
- File dữ liệu JSON thô: `ceh_<target>_<timestamp>.json`
- File giao diện trực quan HTML: `ceh_<target>_<timestamp>.html`
