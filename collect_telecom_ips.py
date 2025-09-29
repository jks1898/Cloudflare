from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import os

# ---------- 配置浏览器 ----------
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无界面模式
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # ---------- 打开网页 ----------
    driver.get('https://ip.164746.xyz/')
    time.sleep(5)  # 等待页面渲染完成

    # ---------- 获取网页内容 ----------
    page_content = driver.page_source

finally:
    driver.quit()

# ---------- 匹配 IPv4 ----------
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

all_ips = sorted(set(re.findall(ip_pattern, page_content)))

# ---------- 测试 IP 是否可用 ----------
def ping_ip(ip):
    param = "-n" if os.name == "nt" else "-c"
    response = os.system(f"ping {param} 1 {ip} >nul 2>&1")
    return response == 0

valid_ips = []
for ip in all_ips:
    if ping_ip(ip):
        valid_ips.append(ip)
    if len(valid_ips) >= 5:  # 找到 5 个可用 IP 就停止
        break

# ---------- 写入文件 ----------
with open("addressesapi.txt", "w") as f:
    for ip in valid_ips:
        f.write(f"{ip} #CT\n")

print(f"共抓取 {len(all_ips)} 个 IP，写入 {len(valid_ips)} 个可用 IP")
