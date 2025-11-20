import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Tải các biến môi trường từ file .env
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "thuetool_data"
COL_NAME = "accounts"

START_DISPLAY_ORDER = 
END_DISPLAY_ORDER = 32

def pause_accounts():
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
        count = 0
        for display_order in range(START_DISPLAY_ORDER, END_DISPLAY_ORDER + 1):
            acc = col.find_one({"displayOrder": display_order})
            if acc:
                col.update_one({"displayOrder": display_order}, {"$set": {"status": "paused", "updatedAt": datetime.now(pytz.utc)}})
                print(f"✅ Đã chuyển tài khoản displayOrder={display_order} sang 'paused'.")
                count += 1
            else:
                print(f"⚠️ Không tìm thấy tài khoản displayOrder={display_order}.")
        print("-" * 30)
        print(f"Tổng số tài khoản đã chuyển trạng thái: {count}")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()
            print("Đã đóng kết nối MongoDB.")

if __name__ == "__main__":
    pause_accounts()
