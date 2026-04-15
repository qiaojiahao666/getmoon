# getmoon
存放python脚本，必要逻辑以及主结构为手写，改错借用了csdn以及ai
# Web 安全学习项目 | 2 个月实习冲刺计划交付物

本仓库是《2个月Web安全实习冲刺「每日落地计划」》的核心代码交付集合。包含了从 CTF 向实战思维转换过程中，独立编写的 Python 安全脚本，涵盖 SQL 盲注自动化、信息收集综合工具、漏洞批量检测三大模块。

**关键词**：`Python` `Web安全` `渗透测试` `多线程` `代理池` `SRC`

---

## 📁 项目结构
.
├── boolean_blind_sqli.py # Day4: 布尔盲注自动化爆破脚本（带 WAF 绕过模块）
├── info_collect.py # Day6: 信息收集综合脚本（子域名/端口/CMS/敏感信息）
├── thinkphp_poc.py # Day8: ThinkPHP 5 RCE 批量检测脚本（多线程 + 在线代理池）
├── poc.txt # POC 目标列表（示例）
└── README.md # 项目说明文档

text

---

## 🐍 环境依赖

所有脚本基于 Python 3.8+ 开发，推荐使用 Python 3.11。

### 通用依赖安装
```bash
pip install requests
部分脚本使用标准库，无需额外安装。

🔧 脚本详解
1. 多线程waf绕过自动化bool盲注脚本(auto_bool.py)
功能描述：

针对 SQLi-Labs Less-8 类型布尔盲注的自动化利用脚本。

支持逐字符爆破 数据库名 → 表名 → 列名 → 数据 的完整流程。

内置多种 WAF 绕过函数（双写、空格替换、URL 编码、注释拆分），可按需调用。

多线程并发爆破，极大提升猜解速度。

使用方法：

修改脚本中的 url 变量为目标靶场地址。

根据目标调整 burp0_headers 请求头。

运行脚本：

bash
python boolean_blind_sqli.py
控制台将实时输出爆破进度及最终结果。

核心代码片段：

python
# 判断页面真假的回调函数
def is_true(payload):
    resp = requests.get(url, params={"id": payload}, headers=burp0_headers)
    return "You are in" in resp.text

# 多线程爆破数据库名长度
for i in range(1, length+1):
    threading.Thread(target=dataname, args=(i,)).start()
2. 信息收集脚本(auto_information_collect.py)
功能描述：

子域名爆破：基于字典文件，通过 DNS 解析发现存活子域名。

端口扫描：分片多线程扫描目标 IP 的常用端口（1-5000）。

CMS 指纹识别：内置 10+ 常见 CMS 指纹（ThinkPHP、WordPress、Discuz 等），通过路径和关键字双重匹配。

敏感信息提取：正则匹配页面中的手机号、身份证、AK/SK 密钥、JS 文件链接。

使用方法：

准备子域名字典文件（ziyuming.txt）。

在 __main__ 中修改 url 为目标主域名。

按需取消注释端口扫描、CMS 识别模块。

运行脚本：

bash
python info_collect.py
模块化设计：

各功能相互独立，可通过注释灵活启用/禁用。

线程锁保证多线程输出序号准确。

指纹库示例：

python
CMS_FINGER = {
    "ThinkPHP": [
        {"path": "/thinkphp/", "keyword": "ThinkPHP"},
        {"path": "/vendor/", "keyword": "think"},
    ],
    "WordPress": [
        {"path": "/wp-includes/", "keyword": "wp-content"},
    ],
    # ... 更多指纹可自行扩展
}
3. ThinkPHP 5 RCE 批量检测脚本 (thinkphp5_poc.py)
功能描述：

针对 ThinkPHP 5.x 远程代码执行漏洞 的批量验证工具。

包含两个经典 POC 路径：

invokefunction 调用 phpinfo

Request/input 过滤器执行 phpinfo

集成 在线代理池（proxy.scdn.io），每次请求随机更换代理 IP，有效防止扫描 IP 被 WAF 封禁。

支持多线程并发，可自定义线程数。

自动记录漏洞 URL 到 vuln_result.txt。

使用方法：

将目标 URL 逐行写入 poc.txt（支持 HTTP/HTTPS、带端口）。

运行脚本：

bash
python thinkphp_poc.py
扫描完成后，存在漏洞的 URL 会输出 [+] 漏洞存在，并保存至结果文件。

代理池设计亮点：

python
# 从在线 API 获取可用代理列表并缓存
def fetch_proxies(count=10, protocol="http"):
    resp = requests.get(PROXY_API, params={"protocol": protocol, "count": count})
    return resp.json()["data"]["proxies"]

# POC 请求时随机选用代理
proxy = random.choice(proxy_list)
proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
requests.get(pocurl, proxies=proxies, timeout=8)
🚀 学习路径与复盘
本仓库代码严格对应《2个月Web安全实习冲刺》计划的关键节点：

天数	交付物	核心收获
Day4	布尔盲注脚本	掌握盲注自动化原理、多线程编程、WAF 绕过基础
Day6	信息收集综合脚本	整合子域名、端口、CMS、敏感信息，形成渗透前置工具链
Day8	ThinkPHP RCE POC	实现 POC 批量验证、在线代理池集成、工程化脚本编写
每一份代码均由本人独立编写、调试、优化，遇到环境问题（如本地代理池搭建失败）时，灵活切换为在线 API 方案，体现了解决实际问题的能力。

📌 免责声明
本仓库代码仅用于网络安全技术学习、授权测试及教学研究。严禁在未获得授权的情况下对任何目标进行扫描、渗透或攻击。使用者需遵守当地法律法规，任何违法滥用行为与本项目作者无关。

📧 联系我
GitHub：[你的 GitHub 主页链接]

博客/笔记：（可选）

如果本项目对你有帮助，欢迎给个 ⭐ Star 支持！

text

### 📌 使用说明

1. 将上述内容复制到你的项目根目录，保存为 `README.md`。
2. 将 `[你的 GitHub 主页链接]` 替换成你自己的 GitHub 地址。
3. 根据实际文件命名调整脚本名称（如你的盲注脚本文件名是否完全一致）。
4. 提交到 GitHub：
   ```bash
   git add README.md
   git commit -m "Add comprehensive README for all three core scripts"
   git push
