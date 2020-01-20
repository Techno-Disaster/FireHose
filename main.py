import requests
import time
import sqlite3
import html2text
import html


conn = sqlite3.connect('firehose.db')
c = conn.cursor()
c.execute(
    "create table if not exists votes (time integer, article_id integer, uid integer);")
c.execute("create table if not exists comments (time integer, comment_id integer, uid integer, article_link text, comment_link text, comment_text text);")
c.execute(
    "create table if not exists articles (time integer, article_id integer, uid integer, article_title text, article_link text, sub_name text, num_votes integer, num_comments integer);")
c.execute("create table if not exists users (uid integer, username text)")
conn.commit()

prev_last_time = time.time()

output = ["type", "votes", "com", "title"]
print("Time            Action  Votes Com   Title")

while True:
    response = requests.get(
        "https://www.meneame.net/backend/sneaker2?time=" + str(prev_last_time))
    events = response.json()["events"]
    for event in events:
        if event["type"] == "vote":
            c.execute("insert into votes values (?, ?, ?);",
                      (event["ts"], event["id"], event["uid"]))
            c.execute("update articles set num_votes=? where article_id=?;",
                      (event["votes"], event["id"]))
        elif event["type"] == "comment":
            comment_text = html2text.HTML2Text().handle(requests.get(
                "https://www.meneame.net/backend/get_comment?id=" + event["id"]).text)
            article_link = event["link"].rsplit('/', 1)[0]
            c.execute("insert into comments values (?, ?, ?, ?, ?, ?);", (
                event["ts"], event["id"], event["uid"], article_link, event["link"], comment_text))
            c.execute("update articles set num_comments=? where article_link=?;",
                      (event["com"], article_link))
        elif event["type"] == "cedited":
            comment_text = html2text.HTML2Text().handle(requests.get(
                "https://www.meneame.net/backend/get_comment?id=" + event["id"]).text)
            c.execute("update comments set comment_text=? where comment_id=?;",
                      (comment_text, event["id"]))
        elif event["type"] == "new":
            c.execute("insert into articles values (?, ?, ?, ?, ?, ?, 0, 0);", (
                event["ts"], event["id"], event["uid"], event["title"], event["link"], event["sub_name"]))

        if event["uid"] != '0' and not c.execute("select uid from users where uid=?;", (event["uid"],)).fetchone():
            c.execute("insert into users values (?, ?);",
                      (event["uid"], event["who"]))

        conn.commit()

        print(time.strftime("%H:%M:%S", time.localtime(
            int(event["ts"]))), end="\t")
        print("\t".join(html.unescape(
            str(event[item])) for item in output))
        prev_last_time = max(int(event["ts"]), prev_last_time)
