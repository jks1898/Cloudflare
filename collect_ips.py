import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 使用集合存储IP地址实现自动去重
unique_ips = set()

for url in urls:
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url, timeout=5)
        
        # 确保请求成功
        if response.status_code == 200:
            # 获取网页的文本内容
            html_content = response.text
            
            # 使用正则表达式查找IP地址
            ip_matches = re.findall(ip_pattern, html_content, re.IGNORECASE)
            
            # 将找到的IP添加到集合中（自动去重）
            unique_ips.update(ip_matches)
    except requests.exceptions.RequestException as e:
        print(f'请求 {url} 失败: {e}')
        continue

# 将去重后的IP地址按数字顺序排序
if unique_ips:
    # 按IP地址的数字顺序排序（非字符串顺序）
    sorted_ips = sorted(unique_ips, key=lambda ip: [int(part) for part in ip.split('.')])
    
    # 定义不同运营商的端口列表
    tsl_ports = ["443", "8443", "2053", "2083", "2087", "2096"]
    
    # 定义notslip.txt使用的端口列表
    notsl_ports = ["80", "8080", "8880", "2052", "2082", "2086", "2095"]
    
    # 创建结果字符串
    result = []
    
    # 从网页内容中提取运营商信息
    mobile_ip = None
    union_ip = None
    telecom_ip = None
    
    # 重新请求网页获取完整内容，包括运营商信息
    try:
        response = requests.get(urls[0], timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找表格行
            rows = soup.find_all('tr')
            
            # 遍历表格行查找运营商信息
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # 第一列通常是运营商名称，第二列是IP地址
                    carrier = cells[0].get_text().strip()
                    ip_cell = cells[1].get_text().strip()
                    
                    # 从单元格文本中提取IP地址
                    ip_match = re.search(ip_pattern, ip_cell)
                    if ip_match:
                        ip = ip_match.group(0)
                        
                        # 根据运营商名称分类
                        if '移动' in carrier and not mobile_ip:
                            mobile_ip = ip
                        elif '联通' in carrier and not union_ip:
                            union_ip = ip
                        elif '电信' in carrier and not telecom_ip:
                            telecom_ip = ip
            
            # 如果没有找到特定运营商的IP，使用前三个IP作为备选
            if not mobile_ip and len(sorted_ips) > 0:
                mobile_ip = sorted_ips[0]
            
            if not union_ip and len(sorted_ips) > 1:
                union_ip = sorted_ips[1]
            
            if not telecom_ip and len(sorted_ips) > 2:
                telecom_ip = sorted_ips[2]
                
    except Exception as e:
        print(f'解析运营商信息失败: {e}')
        
        # 如果解析失败，使用前三个IP作为备选
        if len(sorted_ips) > 0:
            mobile_ip = sorted_ips[0]
        if len(sorted_ips) > 1:
            union_ip = sorted_ips[1]
        if len(sorted_ips) > 2:
            telecom_ip = sorted_ips[2]
    
    # 为找到的IP添加端口信息
    if mobile_ip:
        for port in tsl_ports:
            result.append(f"{mobile_ip}:{port}#移动")
    
    if union_ip:
        for port in tsl_ports:
            result.append(f"{union_ip}:{port}#联通")
    
    if telecom_ip:
        for port in tsl_ports:
            result.append(f"{telecom_ip}:{port}#电信")
    
    # 写入文件
    with open('ip.txt', 'w', encoding='utf-8') as file:
        for line in result:
            file.write(line + '\n')
    
    # 创建notslip.txt文件内容
    notslip_result = []
    
    # 为每个IP添加notsl_ports中的所有端口，并带上运营商信息
    if mobile_ip:
        for port in notsl_ports:
            notslip_result.append(f"{mobile_ip}:{port}#移动")
    
    if union_ip:
        for port in notsl_ports:
            notslip_result.append(f"{union_ip}:{port}#联通")
    
    if telecom_ip:
        for port in notsl_ports:
            notslip_result.append(f"{telecom_ip}:{port}#电信")
    
    # 检查notslip.txt文件是否存在，如果存在则删除它
    if os.path.exists('notslip.txt'):
        os.remove('notslip.txt')
    
    # 写入notslip.txt文件
    with open('notslip.txt', 'w', encoding='utf-8') as file:
        for line in notslip_result:
            file.write(line + '\n')
    
    print(f'已保存 {len(result)} 条IP地址和端口信息到ip.txt文件。')
    print(f'已保存 {len(notslip_result)} 条IP地址和端口信息到notslip.txt文件。')
    print(f'移动IP: {mobile_ip}')
    print(f'联通IP: {union_ip}')
    print(f'电信IP: {telecom_ip}')
else:
    print('未找到有效的IP地址。')
