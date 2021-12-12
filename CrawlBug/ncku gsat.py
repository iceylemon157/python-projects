import requests
import schedule
from time import time, sleep
from datetime import datetime
from secret_token import secret_token, secret_token2

sent = False
count = 2013

def crawl():

    global sent, count

    ncku_csie_url = 'https://www.csie.ncku.edu.tw/ncku_csie/'
    r = requests.get(ncku_csie_url)
    html = r.content.decode()

    ncku_csie_url_id = 'https://www.csie.ncku.edu.tw/ncku_csie/announce/view/' + str(count)
    r2 = requests.get(ncku_csie_url_id)
    html2 = r2.content.decode()

    ncku_csie_url_id2 = 'https://www.csie.ncku.edu.tw/ncku_csie/announce/news/1000'
    r3 = requests.get(ncku_csie_url_id2)
    html3 = r3.content.decode()

    # a = str(datetime.today())[:10]

    if "特殊選才資訊" in html3 and not sent:
        line_send_notify('成大特殊選才資訊!!')
        line_send_notify(ncku_csie_url_id2)
        sent = 1

    if "NCKU CSIE can't find that page." not in html2:
        line_send_notify('成大有新訊息')
        line_send_notify(ncku_csie_url_id)
        count += 1

def line_send_notify(*text):

    line_notify_api = "https://notify-api.line.me/api/notify"
    
    headers = {
        "Authorization": "Bearer " + secret_token2,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    message = '\n'
    for txt in text:
        message += txt + ' '

    params = {"message": message}

    r = requests.post(line_notify_api, headers=headers, params=params)

    print('notification sent\n' if r.status_code == 200 else r.status_code)

if __name__ == '__main__':
    while True:
        crawl()
        sleep(1)
