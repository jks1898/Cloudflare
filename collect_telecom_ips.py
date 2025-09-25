import requests
import re
import os

# 目标URL列表
urls = [
    'https://ip.164746.xyz', 
    'https://cf.090227.xyz', 
    'https://stock.hostmonit.com/CloudFlareYes',
    'https://www.wetest.vip/page/cloudflare/address_v4.html'
]

# 正则表达式匹配IP地址
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 如果 ip.txt 存在，先删除
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 存储去重后的IP
unique_ips = set()

# 从网页中获取IP并筛选出电信相关的IP
for url in urls:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            html_content = response.text
            ip_matches = re.findall(ip_pattern, html_content)
            unique_ips.update(ip_matches)
    except requests.exceptions.RequestException as e:
        print(f'请求 {url} 失败: {e}')

# 假设我们已经确认电信节点的 IP（假设是所有符合“电信”相关规则的 IP）
# 这里用前5个节点作为示例
telecom_ips = list(unique_ips)[:5]  # 只选取前5个电信IP
output_ips = [f"{ip} # 狮城" for ip in telecom_ips]

# 按IP数字顺序排序
sorted_ips = sorted(output_ips, key=lambda ip: [int(part) for part in ip.split()[0].split('.')])

# 写入 ip.txt
with open('ip.txt', 'w') as f:
    for ip in sorted_ips:
        f.write(ip + '\n')

print(f'已保存 {len(sorted_ips)} 个电信IP（备注为狮城）到 ip.txt 文件。')
