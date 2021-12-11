import requests
import smtplib
import schedule
from time import time, sleep
from datetime import datetime

sent = False

def send_mail():
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.set_debuglevel(True)

    smtp.starttls()
    
    account = ''
    password = ''
    
    smtp.login(account, password)
        
    from_addr = ''
    to_addr = ''
    msg="Fubuki is my Waifu"

    status=smtp.sendmail(from_addr, to_addr, msg)
    
    if status=={}: print("郵件傳送成功!")
    else: print("郵件傳送失敗!")

    smtp.quit()


def crawl():
    r = requests.get('https://dcs.site.nthu.edu.tw/app/index.php?Action=mobileloadmod&Type=mobile_rcg_mstr&Nbr=6454')
    html = r.text
    # print(r.text)
    if '2021-12-10' in html:
        print('find date')
        send_mail()


if __name__ == '__main__':
    while True:
        start_time = time()
        sleep(60 - (time() - start_time) % 60)
        crawl()
        if sent: break
