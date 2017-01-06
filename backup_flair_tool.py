import sys, getopt, praw, json

def main(argv):
    outputfile = ''
    subreddit = ''
    try:
        opts, args = getopt.getopt(argv,"s:o:",["subreddit=","ofile="])
    except getopt.GetoptError:
        print 'backup_flair.py -s <subreddit> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--subreddit"):
            subreddit = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print(subreddit)
    print(outputfile)
    reddit = praw.Reddit(client_id = "XXXXX", client_secret = "YYYYY",
            username = "NNNNN", password = "MMMMMM",
            user_agent = "Flair backup for " + subreddit)    
    results = []
    for f in reddit.subreddit(subreddit).flair(limit=None):
        u = f['user'].name
        t = "" if 'flair_text' not in f or not f['flair_text'] else f['flair_text']
        c = "" if 'flair_css_class' not in f or not f['flair_css_class'] else f['flair_css_class']
        results.append([u,t,c])
    with open(outputfile, 'w') as outfile:
        json.dump(results, outfile)
if __name__ == "__main__":
    main(sys.argv[1:])
