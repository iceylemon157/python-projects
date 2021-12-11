import requests
from secret_token import secret_token

def line_send_notify():

    line_notify_api = "https://notify-api.line.me/api/notify"
    
    headers = {
        "Authorization": "Bearer " + secret_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": "FBK is so cute<3."}

    r = requests.post(line_notify_api, headers=headers, params=params)

    print(r.status_code)

if __name__ == '__main__':
    line_send_notify()        
        