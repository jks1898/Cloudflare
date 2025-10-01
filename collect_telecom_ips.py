import requests
from bs4 import BeautifulSoup
import re

# ---------- 配置 ----------
url = "https://www.wetest.vip/page/cloudflare/total_v4.html"
fixed_domains = ["cf.090227.xyz#CT", "ct.877774.xyz#CT"]
output_file = "addressesapi.txt"

# ---------- 请求网页 ----------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
resp = requests.get(url, headers=headers, timeout=10)
resp.raise_for_status()

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

# ---------- 按延迟升序排序 ----------
ip_delay_list.sort(key=lambda x: x[1])

# ---------- 取前三个网页抓取 IP ----------
top_ips_from_web = [ip for ip, _ in ip_delay_list[:3]]

# ---------- 合并最终列表 ----------
final_list = fixed_domains + [f"{ip}#CT" for ip in top_ips_from_web]

# ---------- 写入文件 ----------
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in final_list:
        f.write(f"{entry}\n")

print(f"addressesapi.txt 已更新，内容如下：{final_list}")
