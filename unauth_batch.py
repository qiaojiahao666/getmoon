import requests        #导入请求库
from concurrent.futures import ThreadPoolExecutor 
requests.packages.urllib3.disable_warnings()
from urllib3.exceptions import InsecureRequestWarning
import os              #要用到系统命令



vulns=[]                 #定义两个空列表，分别存储结果和测试url
targets=[]
fales_keyword=["登录","请登录","401","403","unauthorized","forbidden","login"]                   #返回页面无效关键词
yes_keyword=["root", "password", "config", "user", "admin", "list", "info", "订单", "用户"]      #返回页面有效关键词


headers = {"User-Agent": "Mozilla/5.0"}         #添加请求头
def fuzz(url):                                  #单个url漏洞检测
    try:
        # 修复：使用请求头，防止被拦截
        resp=requests.get(url,headers=headers,verify=False,timeout=5) 
        content=resp.text.lower()               #转换为小写，防止大小写不一致
        for nokeys in fales_keyword:            #读取无效关键词
            if nokeys.lower() in content:       #转小写保证变量统一
                print (url,"未发现漏洞")
                return None
        for keys in yes_keyword:               #读取有效关键词
            if keys.lower() in content:
                result=url+"存在未授权漏洞,状态码为"+f"{resp.status_code}" 
                print(result)
                return result
        print(url, "未发现漏洞（页面无敏感信息）")
        return None
    # 修复：规范异常处理
    except Exception:
        print(url, "请求失败/超时")
        return None

def urlget():
    global targets
    url="https://www.test.com"
    # 修复：文件存在判断，防止testurl.txt不存在报错
    if os.path.exists("testurl.txt"):
        with open("testurl.txt","r",encoding="utf-8") as f: #打开存有测试url的文件
            for i in f:
                path=i.strip()                              #除去换行符
                targets.append(url+path)                    #将其加入url列表

    # 修复：移除硬编码绝对路径 → 通用相对路径
    os.system(f"python JSFinder.py -u {url} -ou ftesturl.txt 2>nul")
    # 修复：文件存在判断，防止ftesturl.txt不存在报错
    if os.path.exists("ftesturl.txt"):
        with open("ftesturl.txt","r",encoding="utf-8") as f:
            for i in f:                                    
                path=i.strip()
                targets.append(path)
    targets = list(set(targets))                          
if __name__ == "__main__":
    urlget()
    with ThreadPoolExecutor(max_workers=5) as executor:                  #创建最大线程为5的线程池
        results = executor.map(fuzz,targets)   #等同于我用for循环遍历里面的的内容,创建子进程然后传给函数，但是最大线程为20
        for res in results:                    
            if res:
                vulns.append(res)
    # 修复：自动清理临时文件
    if os.path.exists("ftesturl.txt"):
        os.remove("ftesturl.txt")
    print("\n===== 扫描完成 =====")
    print("发现漏洞：", len(vulns))



