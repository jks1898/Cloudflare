import requests
import re

# 目标 URL
url = 'https://www.wetest.vip/page/cloudflare/total_v4.html'

# 匹配 IPv4 地址的正则
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

try:
    # 请求网页内容
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    html_content = response.text

    # 提取所有 IP
    ips = re.findall(ip_pattern, html_content)

    # 覆盖写入 addressesapi.txt，保留原始顺序
    with open('addressesapi.txt', 'w', encoding='utf-8') as f:
        for ip in ips:
            f.write(f"{ip} #CT\n")

    print(f"共抓取 {len(ips)} 个 IP，已写入 addressesapi.txt 文件。")

except requests.exceptions.RequestException as e:
    print(f"请求 {url} 失败: {e}")
