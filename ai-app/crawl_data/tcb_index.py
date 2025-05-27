import requests
import pandas as pd

import requests

url = "https://api-finfo.vndirect.com.vn/v4/stock_intraday_latest?q=code:TCB&sort=time&size=1000000"

payload = {}
headers = {
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJpc3N1ZXIiLCJzdWIiOiJzdWJqZWN0IiwiYXVkIjpbImF1ZGllbmNlIiwiaW9zIiwib25saW5lIiwidHJhZGVhcGkiLCJhdXRoIl0sImV4cCI6MTc0ODAxODY3OSwibmJmIjoxNzQ3OTg5ODE5LCJpYXQiOjE3NDc5ODk4NzksInZlcmlmeURldmljZUlkIjp0cnVlLCJpc1N0YWZmIjpmYWxzZSwicm9sZXMiOiJbXSIsImFjY291bnRUeXBlIjoiVW5rbm93biIsInZfdXNlcklkIjoiMjEwMTYwMDQ4MTIwNzc2OSIsInVzZXJJZCI6Im51bGwiLCJ2ZXJzaW9uIjoiVjIiLCJjdXN0b21lck5hbWUiOiJOZ3V54buFbiBI4buTbmcgUXXDom4iLCJjb3Jwb3JhdGVJZCI6bnVsbCwidHJhZGluZ0V4cCI6MTc0ODAxODY3MiwiaWRnSWQiOm51bGwsImN1c3RvbWVyVHlwZSI6WyJTRUcwMDAwMDEiXSwicGhvbmUiOiIwMzcyNDAyNjY4IiwiY3VzdG9tZXJJZCI6IjAwMDEyOTk0MzIiLCJzZWdtZW50YXRpb24iOm51bGwsInJldGlyZWRBY2NvdW50cyI6W10sInVzZXJUeXBlIjoiYWN0aXZlIiwiZW1haWwiOiJxdWFucHhobkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6InF1YW4wMTI5Iiwic3RhdHVzIjoiQUNUSVZBVEVEIiwiaXNCbG9ja1RyYWRlIjpmYWxzZX0.LRllCTMHSLCy6aZ5eKaMFSzgtjn8tH0EIX5lP834MHfZf6-UkJUvAbt30bihLhV9OdBBHqktg3m5I9qbJkQGaWmhQ-6I3q8PWbzeZs5n9vSaE6UnS2jqy-OvolxiU-I-FeMKuLGxqBftvO9sdposgyEfGIxMBlMTMEZclnWNSxldYmnVZxZGPEmTGQKomGZm7A84eiKazgDVykB9IGnmewErRIt1C8NXtkOm1Z6fDF0BYLmUggVG7Zmlj9rjZU9l4Tsl5K_fyPQAZ3v8YeWL2g1p4NZ1jwDkrPFuXUakvbVZTHc4uFUTL6rEr_aGZz-J5j4CyYb1lUWliqcgemmr3g'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Bước 2: Kiểm tra và xử lý dữ liệu
if response.status_code == 200:
    json_data = response.json()
    if "data" in json_data:
        df = pd.DataFrame(json_data["data"])
        df.to_csv("stock_data.csv", index=False)
        print("Dữ liệu đã được lưu vào stock_data.csv")
    else:
        print("Không tìm thấy key 'data' trong JSON.")
else:
    print(f"Gọi API thất bại. Mã lỗi: {response.status_code}")
