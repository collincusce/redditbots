import praw, re, requests
from string import Template
from bots.database import Database, Comment, Submission
from bots.bot import Bot

class UFK(Bot):
    def __init__(self, subreddit, username, password, client_id, client_secret, refresh_rate, dbroot, response_root, css_class, css_ignores, bonus_css):
        self.class_key = "UFK"
        self.css_class = css_class
        self.css_ignores = css_ignores
        self.bonus_css = bonus_css
        self.response_root = response_root
        super(UFK, self).__init__(subreddit, username, password, client_id, client_secret, refresh_rate, dbroot)

    def check_comments(self):
        comments = self.home.comments(limit=200)
        for comment in comments:
            if not Comment.is_parsed(comment.id, self.db.session) and comment.author:
                can_award = False
                user_from = comment.author
                if self.check_command(comment):
                    parsed_request = self.parse_comment(comment)
                    if parsed_request['error'] is None:
                        user_to = parsed_request['user_to']
                        if not Award.already_awarded(comment.submission.id, user_from, user_to, self.db.session):
                            can_award = self.add_karma(user_to)
                            if can_award:
                                if user_to.name == self.username:
                                    self.response_handler(comment, 'awarded_bot', parsed_request)
                                else:
                                    self.response_handler(comment, 'awarded', parsed_request)
                            else:
                                self.response_handler(comment, 'cannot_award', parsed_request)
                        else:
                            self.response_handler(comment, 'already_awarded', parsed_request)
                    else:
                        self.response_handler(comment, parsed_request['error'], parsed_request)
                #these next lines must come last in case of network failure from reddit throwing an error
                Comment.add(comment.id, self.db.session)
                if can_award:
                    Award.add(comment.submission.id, user_from, user_to, self.db.session)

    def add_karma(self, user):
        flair = self.home.flair(redditor=user).next()
        if flair and flair['flair_text']:
            foundnum = re.findall(r'\d+', flair['flair_text'])
            if isinstance(foundnum, list) and len(foundnum) > 0:
                num = int(foundnum[0])
            else:
                num = 0
        else:
            num = 0
        num += 1
        flair_text =  "+" + str(num) + " Karma"
        bcss = ""
        for b in sorted(self.bonus_css, key= lambda x: x[0]):
            if num >= b[1]:
                bcss = b[0]
        if flair and flair['flair_css_class'] not in self.css_ignores:
            flair_css = str(self.css_class + " " + bcss).strip()
        else:
            return False
        self.home.flair.set(redditor=user, text=flair_text, css_class=flair_css)
        return True

    def check_command(self, comment):
        if comment.body.lower().strip().startswith("+karma"):
            return True
        return False

    def parse_comment(self, comment):
	parsed_request = {}
        parsed_request['error'] = None
        parsed_request['submission_id'] = comment.submission.id
        parsed_request['user_from'] = comment.author
        parsed_request['subreddit'] = self.subreddit
        if not comment.is_root:
            parent_comment = comment.parent()
            parsed_request['user_to'] = parent_comment.author
            if parsed_request['user_from'] is None or parsed_request['user_to'] is None or not self.verify_negotiation(parsed_request['user_from'],
                                        parsed_request['user_to'], comment, parent_comment):
                parsed_request['error'] = "no_evidence"
            if comment.author == parent_comment.author:
                parsed_request['error'] = "award_self"
        else:
            parsed_request['error'] = "no_top_level"
        return parsed_request

    def verify_negotiation(self, user_from, user_to, comment, parent_comment):
        current_comment = comment
        found_from = False
        found_to = False
        post_list = []
        pc = parent_comment.submission.comments[0]
        submission_author_name = "spez" if current_comment.submission.author is None else current_comment.submission.author.name
        if submission_author_name == user_from.name and submission_author_name != user_to.name and not self.check_command(parent_comment):
            return True #the OP can send to anyone
        namelist = [x.author.name for x in pc.replies if x.author is not None and x.id != comment.id and x.author.name == user_from.name and not self.check_command(x)]
        if user_from.name in namelist:
            post_list.append(user_from.name)
        while not current_comment.is_root:
            current_comment = current_comment.parent()
            if current_comment.author is not None:
                post_list.append(current_comment.author.name)
        post_list.append(submission_author_name)
        if len(post_list) > 1 and user_to and user_from and hasattr( user_to, "name") and hasattr(user_from, "name"):
            pl = list(reversed(post_list))
            for n in range(len(post_list)):
                if n and pl[n] == user_from.name and pl[n - 1] == user_to.name:
                    found_to = True
                if n and pl[n] == user_to.name and pl[n - 1] == user_from.name:
                    found_from = True
        return (found_from and found_to)

    def response_handler(self, comment, key, parsed_request):
        filein = open(self.response_root + "/" + key + ".tpl")
        src = Template( filein.read() )
        txt = src.substitute(parsed_request)
        comment.reply(txt)

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

class Award(Database.Base):
    __tablename__ = 'awards'
    submission_id = Column(String, primary_key=True)
    user_from = Column(String, primary_key=True)
    user_to = Column(String, primary_key=True)

    def __init__(self, submission_id, user_from, user_to):
        self.submission_id = submission_id
        self.user_from = user_from.name
        self.user_to = user_to.name
    
    @staticmethod
    def add(submission_id, user_from, user_to, session):
        try:
            session.add(Award(submission_id, user_from, user_to))
            session.commit()
        except:
            session.rollback()
            raise
            

    @staticmethod
    def already_awarded(submission_id, user_from, user_to, session):
        return False if session.query(Award).filter(Award.submission_id == submission_id, Award.user_from == user_from.name, Award.user_to == user_to.name).first() is None else True


