from pymongo import MongoClient, ReturnDocument
from datetime import datetime, timedelta
from config import Config

# Khởi MongoClient
db = MongoClient(Config.MONGODB_URI).get_database("thuetool_data")
accounts_collection = db.get_collection("accounts")

def get_accounts_to_process():
    """Tìm các account status='waiting', đồng thời chuyển sang updating ngay khi quét.
    Khi chuyển sang updating sẽ xóa trường available_at để tránh chuyển trạng thái sai."""
    q = {"status": "waiting"}
    accs = list(accounts_collection.find(q))
    ids = [acc['_id'] for acc in accs]
    if ids:
        accounts_collection.update_many(
            {"_id": {"$in": ids}},
            {
                "$set": {"status": "updating", "updatedAt": datetime.now()},
                "$unset": {"available_at": ""}
            }
        )
    print(f"Found {len(accs)} accounts to process and set to updating.")
    return accs

def lock_accounts_for_update(ids: list):
    # Hàm này không còn cần thiết nữa vì đã chuyển updating ngay khi quét
    pass

def update_account_password(acc_id, new_pw):
    """Cập nhật mật khẩu mới, đặt mốc thời gian available_at sau 30 phút kể từ khi đổi mật khẩu."""
    now = datetime.now()
    available_at = now + timedelta(minutes=30)
    accounts_collection.find_one_and_update(
        {"_id": acc_id},
        {"$set": {"password": new_pw, "updatedAt": now, "available_at": available_at}},
        return_document=ReturnDocument.AFTER
    )

def auto_update_available():
    """Tự động chuyển các tài khoản updating đã cập nhật mật khẩu mới (có available_at) sang available nếu đã đến thời điểm available_at."""
    now = datetime.now()
    result = accounts_collection.update_many(
        {"status": "updating", "available_at": {"$lte": now}},
        {"$set": {"status": "available"}}
    )
    if result.modified_count:
        print(f"Đã tự động chuyển {result.modified_count} tài khoản updating (đã đổi mật khẩu) sang trạng thái available.")
