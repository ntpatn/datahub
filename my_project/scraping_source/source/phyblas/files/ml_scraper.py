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
url = "https://phyblas.hinaboshi.com/saraban/kanrianrukhongkhrueang"
base_url = "https://phyblas.hinaboshi.com"

# โหลดหน้าเว็บ
res = requests.get(url)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# เตรียมผลลัพธ์
results = []

# ตรงตาม logic ของ XPath:
# //b/following-sibling::div[1]/a[@target="_blank"]
for b_tag in soup.find_all("b"):
    div = b_tag.find_next_sibling("div")
    if div:
        for a in div.find_all("a", target="_blank"):
            results.append(
                {"หัวข้อ": a.get_text(strip=True), "ลิงก์เต็ม": urljoin(base_url, a["href"])}
            )

# แปลงเป็น DataFrame
df = pd.DataFrame(results)
path = get_save_path("source_phyblas_files_ml.csv", "data")
df.to_csv(path, index=False)
