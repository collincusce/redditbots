from bots.user_flair_karma.ufk import UFK
import threading

class run_ufk(threading.Thread):
    def __init__(self, subreddit, moduser, moduserpass, client_id, client_secret):
        threading.Thread.__init__(self)
        self.ufk = UFK(subreddit, moduser, moduserpass, client_id, client_secret, 10,
               "/opt/redditbots/db", "/opt/redditbots/responses/%s" % subreddit,
               "green", ["red", "mod"], [("tier2", 15),("tier3", 50),("tier4", 100),("tier5",250),("tier6",500)])
    def run(self):
        self.ufk.login()
        self.ufk.run()

threads = []
t1 = run_ufk("SUBBREDDIT1", "SUBREDDIT_BOT_ACCOUNT1", "BOT_ACCOUNT_PASSWORD1", "CLIENT_ID", "CLIENT_SECRET")
t1.start()
threads.append(t1)

t2 = run_ufk("SUBREDDIT2", "SUBREDDIT_BOT_ACCOUNT2", "BOT_ACCOUNT_PASSWORD2", "CLIENT_ID", "CLIENT_SECRET")
t2.start()
threads.append(t2)

for thread in threads:
    thread.join()

