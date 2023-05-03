import praw
from praw.models import MoreComments
import json
from datetime import datetime
import toml
import os
import csv
import time
from prawcore.exceptions import Forbidden
from prawcore.exceptions import ServerError

class RedditPost:
    def __init__(self):
        config = toml.load('config.toml')
        self.reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent'],
        )
        self.subreddit = None

    def set_subreddit(self, subreddit):
        self.subreddit = self.reddit.subreddit(subreddit)

    def flush(self, file_path, contents:list[dict]):
        with open(file_path, "a") as f:
            for content in contents:
                json.dump(content, f, separators=(',', ':'))
                f.write("\n")
        last_time = contents[-1]["time"]
        # print("Last post time:", datetime.fromtimestamp(last_time).strftime("%Y-%m-%d %H:%M:%S"))

    def get_reply(self, target):

        self.count += 1
        reply = {}
        reply["text"] = target.body.replace("\n", " ")
        reply["time"] = target.created_utc
        reply["comments"] = []
        for comment in target.replies:
            if isinstance(comment, MoreComments):
                continue
            reply["comments"].append(self.get_reply(comment))
        return reply

    def get_new(self, submissions_file, file_path):
        self.count = 0
        with open(file_path, "w") as f:
            pass
        i = 0
        posts = []
        with open(submissions_file, "r", encoding="utf8") as f:
            f.readline()
            line = f.readline()
            while line:
                id = line.strip()
                while True:
                    try:
                        submission = self.reddit.submission(id)
                        break
                    except:
                        time.sleep(2)
                try:
                    submission.comments.replace_more(limit=0)
                except Forbidden:
                    # print(f"banned on id:{id}!")
                    line = f.readline()
                    continue
                except ServerError:
                    time.sleep(2)
                    continue
                post = {}
                post["title"] = submission.title
                post["text"] = submission.selftext.replace("\n", " ")
                post["time"] = submission.created
                comments = []
                for comment in submission.comments:
                    if isinstance(comment, MoreComments):
                        continue
                    comments.append(self.get_reply(comment))
                post["comments"] = comments
                posts.append(post)
                i+=1
                if i==30:
                    self.flush(file_path, posts)
                    posts = []
                    i=0
                line = f.readline()
        if i>0:
            self.flush(file_path, posts)
        print(f"count: {self.count}")



if __name__ == '__main__':

    reddit_post = RedditPost()
    data_dir = "all_reddit"
    for root, dirs, files in os.walk(os.path.join(data_dir, "submissions")):
        for file in files:
            if file.endswith(".csv"):
                print(file)
                submissions_file = os.path.join(root, file)
                reddit_post.get_new(submissions_file, os.path.join("./", data_dir, "comments", file[:-3]+"txt"))






