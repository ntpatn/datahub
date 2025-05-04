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


# URL amd base
url = "https://phyblas.hinaboshi.com/saraban/python"
base_url = "https://phyblas.hinaboshi.com"

# load page
res = requests.get(url)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# list of results
results = []

# find <u>
for u_tag in soup.find_all("u"):
    section = u_tag.get_text(strip=True)

    # skip หมวดที่ไม่ต้องการ
    if "แหล่งข้อมูลอ้างอิง" in section:
        continue

    # check <div>
    div = u_tag.find_next_sibling("div")
    if div:
        for a in div.find_all("a", target="_blank"):
            results.append(
                {"หัวข้อ": a.get_text(strip=True), "ลิงก์เต็ม": urljoin(base_url, a["href"])}
            )

# แสดงผลหรือแปลงเป็น DataFrame
df = pd.DataFrame(results)
path = get_save_path("source_phyblas_files_basic_python.csv", "data")
df.to_csv(path, index=False)
