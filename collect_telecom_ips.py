import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配电信IP的正则（CT）
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# ip.txt文件路径
ip_file = 'ip.txt'

# 删除旧文件
if os.path.exists(ip_file):
    os.remove(ip_file)

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    html = response.text

    # 提取所有IP
    ips = re.findall(ip_pattern, html)

    # 只筛选电信IP（CT）
    # 注意：网页中电信IP通常在文本中带有“CT”标识
    ct_ips = []
    for line in html.splitlines():
        if 'CT' in line:
            ct_ips += re.findall(ip_pattern, line)
    # 去重
    ct_ips = list(dict.fromkeys(ct_ips))
    
    # 只取前 5 个
    selected_ips = ct_ips[:5]

    # 按端口优先顺序组合
    ports = [443, 8443, 2053, 2083, 2087, 2096]
    final_list = []
    for ip in selected_ips:
        final_list.append(f"{ip}:{ports[0]}#狮城")  # 默认选443端口

    # 写入文件
    with open(ip_file, 'w') as f:
        for item in final_list:
            f.write(item + '\n')

    print(f"已保存 {len(final_list)} 个狮城电信IP到 {ip_file}。")

except requests.RequestException as e:
    print(f"请求失败: {e}")
