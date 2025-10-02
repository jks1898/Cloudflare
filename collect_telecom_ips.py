import requests
from bs4 import BeautifulSoup

# ---------- 配置 ----------
url = "https://api.urlce.com/cloudflare.html"
output_file = "addressesapi.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# ---------- 请求网页 ----------
try:
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
except requests.RequestException as e:
    print(f"网页请求失败: {e}")
    exit(1)

# ---------- 解析表格 ----------
soup = BeautifulSoup(resp.text, "html.parser")
rows = soup.select("table tbody tr")

电信_ips = []

for row in rows:
    cells = row.find_all("td")
    if len(cells) >= 3:
        线路 = cells[0].get_text(strip=True)  # 第1列：线路
        ip = cells[1].get_text(strip=True)    # 第2列：优选IP
        # 第3列是延迟，不需要处理

        if "电信" in 线路:
            电信_ips.append(f"{ip}#CT")

if not 电信_ips:
    print("未获取到任何 电信优选 IP")
    exit(1)

# ---------- 写入文件 ----------
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in 电信_ips:
        f.write(f"{entry}\n")

print(f"addressesapi.txt 已更新，电信优选IP如下：{电信_ips}")
