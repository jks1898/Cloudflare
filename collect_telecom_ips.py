from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

# ---------- 配置 ----------
url = "https://www.wetest.vip/page/cloudflare/total_v4.html"
fixed_domains = ["cf.090227.xyz#CT", "cf.877774.xyz#CT"]
output_file = "addressesapi.txt"

# ---------- 启动 Chrome 无头模式 ----------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
time.sleep(5)  # 等待 JS 渲染完成

# ---------- 定位表格行 ----------
rows = driver.find_elements("css selector", "table tbody tr")
ip_delay_list = []

for row in rows:
    cells = row.find_elements("tag name", "td")
    if len(cells) >= 4:
        ip = cells[0].text.strip()
        delay_text = cells[3].text.strip()  # 第4列是电信延迟(节点)
        match = re.search(r'(\d+)', delay_text)
        if match:
            ip_delay_list.append((ip, int(match.group(1))))

driver.quit()

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
