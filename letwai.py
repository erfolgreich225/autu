from pymongo import MongoClient
from config import Config

# Kết nối tới database
client = MongoClient(Config.MONGODB_URI)
db = client.get_database("thuetool_data")
accounts_collection = db.get_collection("accounts")

# Chuyển các tài khoản có displayOrder từ 1 đến 24 sang trạng thái waiting
result = accounts_collection.update_many(
    {"displayOrder": {"$gte": 1, "$lte": 24}},
    {"$set": {"status": "waiting"}}
)
print(f"Đã chuyển {result.modified_count} tài khoản sang trạng thái waiting.")
