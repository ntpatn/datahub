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
url = "https://phyblas.hinaboshi.com/saraban/khrong_khai_prasat_thiam"
base_url = "https://phyblas.hinaboshi.com"

# โหลดหน้าเว็บ
res = requests.get(url)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# เตรียมผลลัพธ์
results = []

# ตรงตาม logic ของ XPath:
# //h3[contains(text(),"โครงข่ายประสาท")]/following-sibling::div[1]/a[@target="_blank" and contains(., 'บทที่')]
for h3_tag in soup.find_all("h3"):
    if "โครงข่ายประสาท" in h3_tag.get_text(strip=True):
        div = h3_tag.find_next_sibling("div")
        if div:
            for a in div.find_all("a", target="_blank"):
                if "บทที่" in a.get_text():
                    results.append(
                        {
                            "หัวข้อ": a.get_text(strip=True),
                            "ลิงก์เต็ม": urljoin(base_url, a["href"]),
                        }
                    )

# แปลงเป็น DataFrame
df = pd.DataFrame(results)
path = get_save_path("source_phyblas_files_deeplearning.csv", "data")
df.to_csv(path, index=False)
