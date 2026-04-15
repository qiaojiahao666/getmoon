import socket
import re
import requests
import threading
from queue import Queue
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

found_cms = set()
# 超全CMS指纹库 v2025
# 包含：博客、CMS、论坛、电商、企业站、框架、小众系统 200+

threads = []
threadss = []       
ips = []
count = 1
yuname = []
count_lock = threading.Lock()  # 【修改】用于保护 count 的线程锁

CMS_FINGER = {
    "ThinkPHP": [
        {"path": "/thinkphp/", "keyword": "ThinkPHP"},
        {"path": "/vendor/", "keyword": "think"},
    ],
    "WordPress": [
        {"path": "/wp-includes/", "keyword": "wp-content"},
        {"path": "/wp-login.php", "keyword": "wp-login"},
    ],
    "Typecho": [
        {"path": "/usr/", "keyword": "Typecho"},
        {"path": "/admin/", "keyword": "typecho"},
    ],
    "DedeCMS(织梦)": [
        {"path": "/dede/", "keyword": "DedeCMS"},
        {"path": "/include/", "keyword": "dedecms"},
    ],
    "PHPCMS": [
        {"path": "/phpcms/", "keyword": "PHPCMS"},
    ],
    "Discuz!X": [
        {"path": "/static/", "keyword": "Discuz!"},
    ],
    "SpringBoot": [
        {"path": "/error", "keyword": "Whitelabel"},
    ],
    "ZBlog": [
        {"path": "/zb_users/", "keyword": "ZBlog"},
    ],
    "Emlog": [
        {"path": "/content/", "keyword": "emlog"},
    ],
}

def zym(url, i):
    global count
    global ips
    i = i.strip()
    name = i + "." + url
    try:
        ip = socket.gethostbyname(name)
        # 【修改】加锁确保计数原子性，避免多线程下序号重复/跳号
        with count_lock:
            current = count
            count += 1
        print(current, "---", name, "域名存在------", ip)
        ips.append(ip)
        yuname.append(name)
    except socket.gaierror:
        pass
#敏感信息收集
def gett(url):
    for head in ["https://", "http://"]:
        try:
            resp = requests.get(f"{head}{url}")
            phone = re.findall(r"\b1[3-9][0-9]{9}\b", resp.text)              #手机号码提取    
            print("手机号码:", phone)
            shenfenid = re.findall(r"\b[0-9]{17}[xX0-9]\b", resp.text)        #身份证提取
            print("身份证号码:", shenfenid)
            Acessk = re.findall(r"\b[A-Z]{4}[A-Z0-9a-z]{16}+\b", resp.text)
            print("AK:", Acessk)
            Scessk = re.findall(r"\b[A-Z0-9a-z]{29,32}\b", resp.text)         #简单SK密钥提取             
            print("SK:", Scessk) 
            links = re.findall(r'<script src="(.+?.js)"></script>', resp.text)# JS敏感信息提取
            print("JS:",links)
        except:
            continue
#端口爆破函数      
def nmap(ip, start):
    for i in range(start, start + 100):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((ip, i))
            print(f"端口:{i}存在")
            s.close()
        except:
            pass
#cms指纹识别
def cms(url, head, cms_name, finger):
    payload = f'{head}{url}{finger["path"]}'
    try:
        resp = requests.get(payload, timeout=1, verify=False)
        if resp.encoding is None:
            resp.encoding = resp.apparent_encoding or 'utf-8'
        if resp.status_code == 200 and finger["keyword"] in resp.text:
            found_cms.add(cms_name)
            return
    except:
        pass

if __name__ == "__main__":
    url="www.hzu.edu.cn"                                                               #自定义要爆破的子域名                                                                                                                                                                                                                                 
    with open ("C:/Users/17527/Desktop/test/ziyuming.txt","r",encoding="utf-8")as f:   #打开字典文件
        url=url.replace("www.","")
    # 线程池，最大20线程，不崩溃、不报错
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=20) as executor:
            for i in f:
                executor.submit(zym, url, i)

#爆破查询到的子域名ip端口
"""
    ip="127.0.0.1"                                     #ip改为需要爆破的ip                       
     
    for i in range(1,5000,100):                                   
        tt=threading.Thread(target=nmap,args=(ip,i))   #可以修改nmap对象,修改url就行
        tt.start()
        threadss.append(tt)
    for tt in threadss:
        tt.join()

"""

#查询各端口的cms指纹
"""
    url="ctfhub.com"
    for head in ["https://","http://"]:
        for cms_name, finger_list in CMS_FINGER.items():
            for finger in finger_list:
                ttt=threading.Thread(target=cms,args=(url,head,cms_name, finger))
                ttt.start()
                threads.append(ttt)
    for ttt in threads:
        ttt.join()
    print("\n[+] 识别到CMS:", list(found_cms))
    
 
"""
