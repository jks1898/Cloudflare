from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time

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

html_content = driver.page_source
driver.quit()

# ---------- 正则抓取 IP + 电信延迟(节点) ----------
# 匹配类似 "1.2.3.4" 后面紧跟 "电信延迟(节点)" 和数字
pattern = r'(\b(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
          r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
          r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
          r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b).*?电信延迟\(节点\).*?(\d+)'

matches = re.findall(pattern, html_content, flags=re.S)

# ---------- 转换成列表并按延迟升序 ----------
ip_delay_list = [(ip.strip(), int(delay)) for ip, delay in matches]
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
