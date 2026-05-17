import os
import sys

# 1. Ép buộc thiết lập host và port từ biến môi trường của Render
#    Render tự động tạo biến môi trường PORT (thường là 10000)
os.environ["FASTMCP_HOST"] = "0.0.0.0"
os.environ["FASTMCP_PORT"] = os.environ.get("PORT", "8000")

# 2. Khởi chạy ứng dụng chính
#    Điều này sẽ import và chạy code trong bybit.py
if __name__ == "__main__":
    # Thay thế tiến trình hiện tại bằng lệnh chạy server
    import subprocess
    subprocess.run([sys.executable, "bybit.py", "--transport", "streamable-http"])
