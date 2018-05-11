import praw, re, requests
from string import Template
from bots.database import Database, Comment, Submission
from bots.bot import Bot

class FKS(Bot):
    def __init__(self, subreddit, username, password, client_id, client_secret, refresh_rate, dbroot, syncfunc, syncsubs):
        self.class_key = "FKS"
        self.syncfunc = syncfunc
        self.syncsubs = syncsubs
        super(FKS, self).__init__(subreddit, username, password, client_id, client_secret, refresh_rate, dbroot)

    def check_flair(self):
        allsubs = list(self.syncsubs)
        allsubs.append(self.subreddit)
        users_by_sub = {}
        results_by_sub = {}
        for sub in allsubs:
            flairs = self.reddit.subreddit(sub).flair(limit=None)
            for f in flairs:
                if f['user'] not in users_by_sub:
                    users_by_sub[f['user']] = {}
                users_by_sub[f['user']][sub] = {'css_class': unicode(f.get('flair_css_class') or ''), 'text': unicode(f.get('flair_text') or '')}
        for u in users_by_sub:
            results_by_sub[u] = self.syncfunc(users_by_sub[u], allsubs)
        for u in results_by_sub:
            for sub in results_by_sub[u]:
                t = results_by_sub[u][sub]['text']
                c = results_by_sub[u][sub]['css_class']
                self.reddit.subreddit(sub).flair.set(redditor = u, text = t, css_class = c )
