import requests
import re

# 目标 URL
url = 'https://www.wetest.vip/page/cloudflare/total_v4.html'

# IP 匹配正则
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

try:
    # 请求网页内容
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    html_content = response.text

    # 提取所有 IP
    ips = re.findall(ip_pattern, html_content)

    # 去重并排序
    unique_ips = sorted(set(ips), key=lambda ip: [int(part) for part in ip.split('.')])

    # 写入 addressapi.txt（覆盖保存）
    with open('addressapi.txt', 'w', encoding='utf-8') as f:
        for ip in unique_ips:
            f.write(f"{ip} #CT\n")

    print(f"共抓取 {len(unique_ips)} 个 IP，已写入 addressapi.txt 文件。")

except requests.exceptions.RequestException as e:
    print(f"请求 {url} 失败: {e}")
