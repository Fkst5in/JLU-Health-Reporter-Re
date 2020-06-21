## JLU Health Reporter Re

为吉林大学本科生每日健康情况申报所作的自动机器人。

以 WTFPL 授权开源。Pray for Hubei.

原版：[JLU Health Reporter](https://github.com/TechCiel/jlu-health-reporter)
### 免责声明

本自动程序为个人使用开发，未经充分测试，不保证正常工作。

本自动程序仅适用于 2020 年初 COVID-19 疫情期间吉林大学本科生、研究生健康情况申报及本科生每日打卡，不保证按时更新。

请注意，本自动程序仅会每 24 小时自动重新提交上次提交的内容，**如您的申报内容变化，请立即停止使用本程序！**

__**如运行本程序，您理解并认可，本自动程序的一切操作均视为您本人、或由您授权的操作。**__

### 环境说明

需要 Python 3 ，先 `pip3 install requests` 。

运行之前先登录平台提交一次申报，务必确保信息准确。

把文件开头的 `USERS` 中的示例用户名和密码换为自己的，支持多帐号。

若为**研究生健康申报**使用，请先改变文件开头的 `TRANSACTION` 。

### 参数说明

```
-h [--health] 健康申报
-m [--morning] 早间打卡
-n [--noon] 午间打卡
-a [--afternoon] 下午打卡
-e [--evening] 晚间打卡
```
### 使用说明
Crontab 模式：

```
7 7 * * * username /usr/bin/python3 /绝对路径/jlu-health-reporter.py -h --once >> reporter.log 2>&1
7 7 * * * username /usr/bin/python3 /绝对路径/jlu-health-reporter.py -m --once >> reporter.log 2>&1
7 11 * * * username /usr/bin/python3 /绝对路径/jlu-health-reporter.py -n --once >> reporter.log 2>&1
7 17 * * * username /usr/bin/python3 /绝对路径/jlu-health-reporter.py -a --once >> reporter.log 2>&1
7 21 * * * username /usr/bin/python3 /绝对路径/jlu-health-reporter.py -e --once >> reporter.log 2>&1
```

手动模式：

```
#以本科生健康申报为例
./jlu-health-reporter.py -h
```

### 联系

欢迎开 issue 、pr ，随缘处理。
