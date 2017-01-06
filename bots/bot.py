import praw, time, os, database, sys, traceback

class Bot(object):
    def __init__(self,subreddit, username, password, client_id, client_secret, refresh_rate, dbroot):
        if not hasattr(self, 'class_key'):
            self.class_key = 'default'
        self.subreddit = subreddit
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
	self.subreddit = subreddit
        self.dbpath = dbroot + '/' + self.subreddit
        self.dblocation = self.dbpath + '/' + self.class_key + '.db'
        try:
            os.makedirs(self.dbpath)
        except OSError:
            if not os.path.isdir(self.dbpath):
		raise
	self.db = database.Database(self.dblocation)
        self.refresh_rate = max(10, refresh_rate)
	self.reddit = None

    def login(self):
        if self.reddit is not None:
            self.reddit = None
        self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret,
            username = self.username, password = self.password,
            user_agent = "Karma monster for " + self.subreddit)
        #self.reddit.login(self.username, self.password, disable_warning=True)
        self.home = self.reddit.subreddit(self.subreddit)

    def run(self):
        if self.reddit is None:
            print self.subreddit + "__" + self.class_key + " - Please intialize a subreddit before running."
            return False
        while True:
            time.sleep(self.refresh_rate)
            try:
                self.check_comments()
            except Exception as emsg:
                exc_type, exc_obj, tb = sys.exc_info()
                print self.subreddit + "__" + self.class_key + " - LINE " + str(tb.tb_lineno) + " - Error checking comments: {0}".format(emsg)
                print traceback.format_exc()
            try:
                self.check_submissions()
            except Exception as emsg:
                exc_type, exc_obj, tb = sys.exc_info()
                print self.subreddit + "__" + self.class_key + " - LINE " + str(tb.tb_lineno) + " - Error checking submissions: {0}".format(emsg)
                print traceback.format_exc()
            try:
                self.check_messages()
            except Exception as emsg:
                exc_type, exc_obj, tb = sys.exc_info()
                print self.subreddit + "__" + self.class_key + " - LINE " + str(tb.tb_lineno) + " - Error checking messages: {0}".format(emsg)
                print traceback.format_exc()
            try:
                self.check_flair()
            except Exception as emsg:
                exc_type, exc_obj, tb = sys.exc_info()
                print self.subreddit + "__" + self.class_key + " - LINE " + str(tb.tb_lineno) + " - Error checking flair: {0}".format(emsg)
                print traceback.format_exc()
            
    def check_comments(self):
        pass
    def check_submissions(self):
        pass
    def check_messages(self):
        pass
    def check_flair(self):
        pass
