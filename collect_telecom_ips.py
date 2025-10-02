import requests
from bs4 import BeautifulSoup
import re
import os

# ---------- 配置 ----------
url = "https://www.wetest.vip/page/cloudflare/total_v4.html"
output_file = "addressesapi.txt"

# ---------- 请求网页 ----------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

try:
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
except requests.RequestException as e:
    print(f"网页请求失败: {e}")
    exit(1)

# ---------- 解析表格 ----------
soup = BeautifulSoup(resp.text, "html.parser")
rows = soup.select("table tbody tr")

ip_delay_list = []

for row in rows:
    cells = row.find_all("td")
    if len(cells) >= 4:
        ip = cells[0].get_text(strip=True)
        delay_text = cells[3].get_text(strip=True)
        match = re.search(r'(\d+)', delay_text)
        if match:
            ip_delay_list.append((ip, int(match.group(1))))

if not ip_delay_list:
    print("未获取到任何 IP 信息")
    exit(1)

# ---------- 按延迟升序排序 ----------
ip_delay_list.sort(key=lambda x: x[1])

# ---------- 取前 8 个延迟最低的 IP ----------
top_8_ips = [f"{ip}#CT" for ip, _ in ip_delay_list[:8]]

# ---------- 写入文件（覆盖旧文件） ----------
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in top_8_ips:
            f.write(f"{entry}\n")
    print(f"addressesapi.txt 已更新，内容如下：{top_8_ips}")
except OSError as e:
    print(f"写入文件失败: {e}")
