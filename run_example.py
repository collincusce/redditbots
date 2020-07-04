from bots.user_flair_karma.ufk import UFK
from bots.flair_karma_sync.fks import FKS
import threading
import re

def karmasync(subdict, allsubs):
    maxnum = 0
    maxsub = ""
    results = subdict.copy()
    ignore_classes = ['red', 'mod']
    ignore_subs = dict()
    for s,f in subdict.iteritems():
        if not set(ignore_classes).isdisjoint(f['css_class'].strip().split()):
            ignore_subs[s] = True
        num = 0
        if f['text'] and f['text'].strip():
            foundnum = re.findall(r'\d+', f['text'].strip())
            if isinstance(foundnum, list) and len(foundnum) > 0:
                num = int(foundnum[0])
            else:
                num = 0
        if maxnum < num:
            maxnum = num
            maxsub = s
    for s in allsubs:
        if s not in results:
            results[s] = {'text':'','css_class':''}
        if s in ignore_subs or not maxnum or (results[s]['text'] == subdict[maxsub]['text'] and results[s]['css_class'] == subdict[maxsub]['css_class']):
            results.pop(s)
        else:
            results[s]['text'] = subdict[maxsub]['text']
            results[s]['css_class'] = subdict[maxsub]['css_class']
    return results

class run_fks(threading.Thread):
    def __init__(self, subreddit, moduser, moduserpass, client_id, client_secret, syncfunc, syncsubs):
        threading.Thread.__init__(self)
        self.fks = FKS(subreddit, moduser, moduserpass, client_id, client_secret, 10,
               "/opt/redditbots/db", syncfunc, syncsubs )
    def run(self):
        self.fks.login()
        self.fks.run()

karmasubs = ["relatedsub1" , "relatedsub2", "SUBREDDIT2"]


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

t3 = run_fks("SUBREDDIT1", "GLOBAL_BOT_ACCOUNT", "GLOBAL_BOT_ACCOUNT_PASSWORD", "CLIENT_ID", "CLIENT_SECRET", karmafunc, karmasubs)
t3.start()
threads.append(t3)


for thread in threads:
    thread.join()

