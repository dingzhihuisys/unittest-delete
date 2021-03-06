# @dingzhihui   
# 2021/2/7   
# 4:19 下午   
# PyCharm
import unittest

# 测试用例存放路径
case_path = 'case'
"""
在自动化框架里使用HTMLTestRunner  时:
tests = unittest.defaultTestLoader.discover("./python_test/case", pattern='*.py', top_level_dir=None)
这句话会报错：
Start directory is not importable: './testsuits'
经过网上自己搜索最后解决方案是：再加一个. 改为：
tests = unittest.defaultTestLoader.discover("../python_test/case", pattern='*.py', top_level_dir=None)
OK 啦~~~
"""


# 获取所有测试用例
def get_all_case():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py")
    suite = unittest.TestSuite()
    suite.addTest(discover)
    return suite
    for test_suit in discover:
        for test_case in test_suit:
            # 添加用力到suite
            suite.addTests(test_case)
    print(suite)
    return suite


"""==============================定义邮件============================="""
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import os
from email.mime.multipart import MIMEMultipart


# 定义发送邮件
def send_mail(file_new):
    # -----------1.发件相关内容------------
    smtpserver = 'smtp.downtown8.com'
    port = 0  # 端口
    username = 'zhihui.ding@downtown8.com'  # 发件箱用户名
    password = 'DZH123456@'  # 发件箱密码
    sender = 'zhihui.ding@downtown8.com'  # 发件人邮箱
    # receiver = '1002837527@qq.com'  # 收件人邮箱
    receiver = ['1002837527@qq.com', '609093314@qq.com']

    # -----------2.编辑邮件内容--------------
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    body = MIMEText(mail_body, 'html', 'utf-8')
    # 邮件对象
    msg = MIMEMultipart()
    msg['Subject'] = Header("自动化测试报告", 'utf-8').encode()  # 主题
    msg['From'] = Header(u'测试机器触发 <%s>' % sender)  # 发件人
    print(sender + "0000000000000-------1")
    # msg['to'] = Header(u'收件人 <%s>' % receiver)  # 收件人
    msg['to'] = ';'.join(receiver)
    msg['date'] = time.strftime("%a,%d %b %Y %H:%M:%S %z")  # 日期
    msg.attach(body)
    # 附件
    att = MIMEText(mail_body, 'base64', 'utf-8')
    att['Content-Type'] = "application/octet-stream"
    att['Content-Disposition'] = 'attachment; filename="test_report.html"'
    msg.attach(att)
    # --------------3发送邮件--------------
    try:
        smt_l = smtplib.SMTP()
        # 邮箱服务器 imap.downtown8.com smtp.downtown8.com
        smt_l.connect(smtpserver)
        # 登录邮箱
        smt_l.login(username, password)
    except:
        smt_l = smtplib.SMTP_SSL(smtpserver, port)
        smt_l.login(username, password)
    # 发送者和接受者
    smt_l.sendmail(sender, receiver, msg.as_string())
    # #发送邮件
    # smt_l = smtplib.SMTP()
    # smt_l.connect('smtp.mxhichina.com')  # 邮箱服务器
    # smt_l.login(username, password)  # 登录邮箱
    # smt_l.sendmail(sender, receiver, msg.as_string())  # 发送者和接收者
    smt_l.quit()
    print("邮件已发出 ，注意查收")


"""==============================获取最新的测试报告============================="""


# 查找测试目录 找到最新生成的测试报告文件
def new_report(test_report):
    # 列出目录下所有文件和文件夹保存到lists
    lists = os.listdir(test_report)
    # 按时间排序
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))
    # 获取最新的文件到存到file_new
    file_new = os.path.join(test_report, lists[-1])
    print(file_new)
    return file_new


if __name__ == '__main__':
    # 返回实例
    runner = unittest.TextTestRunner()
    # 导入第三方模块
    from common import HTMLTestRunner
    import time

    # 获取当前时间（每次生成的报表不覆盖）
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # print(time.localtime(time.time()))
    # 保存生成报告的路径
    report_path = "/Users/dingzhihui/dzh_test/pythonProject/python_test/report/result" + now + ".html"
    # report_path = "D:/pythonProject/python_test/report/result" + now + ".html"
    fp = open(report_path, 'wb')

    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='测试用例',
        verbosity=2,
        description='用例执行情况'
    )

    # 运行所有
    runner.run(get_all_case())
    # 关闭文件 记住用open()打开文件后一定要记得关闭它，否则会占用系统的可打开文件句柄数。
    fp.close()
    # 测试报告文件夹
    # test_path = "/Users/dingzhihui/PycharmProjects/python_test/report/"
    test_path = "D:/pythonProject/python_test/report/"
    new_report = new_report(test_path)
    # 发送测试报告
    send_mail(new_report)