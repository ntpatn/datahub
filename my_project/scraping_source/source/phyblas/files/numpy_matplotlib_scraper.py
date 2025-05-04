import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../code"))
)
from save_local import get_save_path

# URL และ base
url = "https://phyblas.hinaboshi.com/saraban/numpy_matplotlib"
base_url = "https://phyblas.hinaboshi.com"

# โหลดหน้าเว็บ
res = requests.get(url)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# เตรียมเก็บผลลัพธ์
results = []

# วนลูปหา <i> ที่มีคำว่า "เนื้อหา" เท่านั้น
for i_tag in soup.find_all("i"):
    section = i_tag.get_text(strip=True)

    if "เนื้อหา" not in section:
        continue  # ข้ามหัวข้ออื่นที่ไม่ใช่เนื้อหา

    # ✅ ดึง <div> ถัดไป แล้วหา <a>
    div = i_tag.find_next_sibling("div")
    if div:
        for a in div.find_all("a", target="_blank"):
            results.append(
                {"หัวข้อ": a.get_text(strip=True), "ลิงก์เต็ม": urljoin(base_url, a["href"])}
            )

# แปลงเป็น DataFrame
df = pd.DataFrame(results)
path = get_save_path("source_phyblas_files_numpy_matplotlib.csv", "data")
df.to_csv(path, index=False)
