import requests
import time
import html
prev_last_time = time.time()

appearing_order = ["type", "votes", "com", "title"]
print("Time            Action  Votes Com   Title")

while True:
    response = requests.get(
        "https://www.meneame.net/backend/sneaker2?time=" + str(prev_last_time))
    events = response.json()["events"]
    for event in events:
        print(time.strftime("%H:%M:%S", time.localtime(
            int(event["ts"]))), end="\t")
        print("\t".join(html.unescape(
            str(event[item])) for item in appearing_order))
        prev_last_time = max(int(event["ts"]), prev_last_time)
