import requests
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = 'https://www.wetest.vip/page/cloudflare/total_v4.html'

# 匹配 IPv4 和电信延迟的正则
ip_pattern = r'(\b(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
             r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
             r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
             r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b).*?电信延迟.*?(\d+)\s*毫秒'

# Session + 重试
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500,502,503,504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

headers = {"User-Agent": "Mozilla/5.0 (compatible; IPCollector/1.0)"}

try:
    response = session.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    html_content = response.text

    # 提取 IP + 延迟
    matches = re.findall(ip_pattern, html_content, flags=re.S)
    ip_delay_list = [(ip, int(delay)) for ip, delay in matches]

    # 按延迟升序排序
    ip_delay_list.sort(key=lambda x: x[1])

    # 取前 8 个 IP
    top_ips = [ip for ip, _ in ip_delay_list[:8]]

    # 写入文件
    with open('addressesapi.txt', 'w', encoding='utf-8') as f:
        for ip in top_ips:
            f.write(f"{ip} #CT\n")

    print(f"抓取 {len(top_ips)} 个延迟最低的 IP 完成。")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
