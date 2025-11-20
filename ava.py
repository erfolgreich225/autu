import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy chuỗi kết nối từ biến môi trường
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "thuetool_data"  # Giả sử DB name không đổi
COL_NAME = "accounts"     # Giả sử Collection name không đổi

def reset_stuck_accounts():
    """
    Đổi trạng thái tất cả các tài khoản từ 'updating' sang 'available'.
    """
    if not MONGODB_URI:
        print("❌ Lỗi: Vui lòng cung cấp biến môi trường MONGODB_URI trong file .env")
        return

    try:
        print("Connecting to MongoDB...")
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        col = db[COL_NAME]
        db.command("ping")
        print("✅ Kết nối MongoDB thành công!")

        # Chỉ cập nhật các tài khoản đang updating
        query = {"status": "updating"}
        new_values = {
            "$set": {
                "status": "available",
                "updatedAt": datetime.now(pytz.utc)
            }
        }
        result = col.update_many(query, new_values)
        print("-" * 30)
        print(f"✅ Đã chuyển trạng thái {result.modified_count} tài khoản từ 'updating' sang 'available'.")

    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()
            print("Đã đóng kết nối MongoDB.")

if __name__ == "__main__":
    reset_stuck_accounts()