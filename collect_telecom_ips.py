import requests
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = 'https://www.wetest.vip/page/cloudflare/total_v4.html'

# 匹配 IPv4 和电信延迟(节点)数据的正则
ip_pattern = r'(\b(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
             r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
             r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.' \
             r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b).*?电信延迟\(节点\).*?(\d+)\s*毫秒'

# Session + 重试
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500,502,503,504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

headers = {"User-Agent": "Mozilla/5.0 (compatible; IPCollector/1.0)"}

try:
    response = session.get(url, headers=headers, timeout=8)
    response.raise_for_status()
    html_content = response.text

    # 提取 IP + 电信延迟(节点)
    matches = re.findall(ip_pattern, html_content, flags=re.S)
    ip_delay_list = [(ip.strip(), int(delay)) for ip, delay in matches]

    # 按电信延迟(节点)升序排序
    ip_delay_list.sort(key=lambda x: x[1])

    # 网页抓取的前三名 IP
    top_ips_from_web = [ip for ip, _ in ip_delay_list[:3]]

    # 固定前两名优选域名
    fixed_domains = ["cf.090227.xyz#CT", "cf.877774.xyz#CT"]

    # 合并成最终列表（前两名固定域名 + 三个网页抓取 IP）
    final_list = fixed_domains + [f"{ip}#CT" for ip in top_ips_from_web]

    # 写入文件
    with open('addressesapi.txt', 'w', encoding='utf-8') as f:
        for entry in final_list:
            f.write(f"{entry}\n")

    print(f"生成 addressesapi.txt，内容如下：{final_list}")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
