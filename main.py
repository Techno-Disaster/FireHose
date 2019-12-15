import requests
from datetime import datetime
from bs4 import BeautifulSoup


def firehose():
    previousts = 0
    duplicateeventts = 0
    ts_duplicate_counter = 1
    while True:
        r = requests.get(
            "https://www.meneame.net/backend/sneaker2")
        data = r.json()  # we get data here.

        listofdata = data["events"]
        reverselist = listofdata[::-1]  # to reverse the list

        for event in reverselist:

            if int(event["ts"]) < int(previousts):
                continue

            if int(event["ts"]) == int(previousts):  # duplicate event.
                ts_duplicate_counter += 1
                if ts_duplicate_counter <= duplicateeventts:
                    continue
            output(event)
            previousts = event["ts"]  # this keeps updating the previous ts.

        duplicateeventts = ts_duplicate_counter
        ts_duplicate_counter = 0  # reset ts counter for next loop


def output(event):
    time = str(datetime.utcfromtimestamp(
        int(event["ts"])).strftime('%Y-%m-%d %H:%M:%S'))
    sub_name = event["sub_name"]
    action = event["type"]
    vote_comments = str(event["votes"]) + "/" + str(event["com"])
    title = event["title"]

    ret = str(BeautifulSoup("{} | {:<10} | {:<10} | {:<8} | {}"
                            .format(time, sub_name, action, vote_comments, title,), 'html.parser'))

    print(ret)


if __name__ == "__main__":
    print("        Time        |    Topic   |   Action   | Comments |   Title   ")
    firehose()
