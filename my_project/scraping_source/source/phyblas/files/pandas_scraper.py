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
url = "https://phyblas.hinaboshi.com/saraban/pandas"
base_url = "https://phyblas.hinaboshi.com"

# โหลดหน้าเว็บ
res = requests.get(url)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# เตรียมเก็บผลลัพธ์
results = []

# วนลูปหา div[2] แล้วกรองเฉพาะ <a target="_blank"> ที่ขึ้นต้นด้วย "บทที่"
divs = soup.find_all("div")
if len(divs) >= 3:  # div[2] หมายถึงลำดับที่ 2 = index 2
    for a in divs[2].find_all("a", target="_blank"):
        text = a.get_text(strip=True)
        if text.startswith("บทที่"):
            results.append({"หัวข้อ": text, "ลิงก์เต็ม": urljoin(base_url, a["href"])})

# แปลงเป็น DataFrame
df = pd.DataFrame(results)
path = get_save_path("source_phyblas_files_pandas.csv", "data")
df.to_csv(path, index=False)
