# reddit-bot

There's actually two bots in this repository: User Flair Karma (UFK) and Flair Karma Sync (FKS). UFK allows users to assign each other karma with people they've had conversations with. FKS synchronises flair between subreddits given any synchronisation algiorithm you provide.

#User Flair Karma (UFK)

UFK is a bot which automatically scans user comments and awards karma when other users indicate they'd like to give them some karma. It updates their user flair to display this karma. It supports any multiple tiers of Karma flair, custom to your liking.

## How does it work?

The bot scans the last 200 comments and looks for a comment that says "+karma". When it sees this comment, it assigns Karma to the assigned user and updates the user's karma. This follows the rules in the UserKarmaGuide.md file. There are an arbitrary number of karma tiers available, and you can assign any CSS class you wish to that. 

There's a root_css class. This is given to any user assigned karma. It's the basic class for adding karma.

ex: "green"

There's also a list of css_ignores. If the bot sees that a person has one of these classes, their karma will not be updated. This is good for moderators and those who have been warned or blacklisted.

ex: ["red", "mod"]

There's also a list of bonus_css classes. This is a list of tuples of size 2. The first tuple is the name of the bonus class with special flair design, and the second is the threshold in which this flair will be assigned. In the below example, css class "tier3" is assigned at 50+ karma, and "tier5" is assigned at 250+ karma. 

ex: [("tier2", 15),("tier3", 50),("tier4", 100),("tier5",250),("tier6",500)]

The bot may run on as many subreddits as you like simultaneously. 

# Flair Karma Sync (FKS)

FKS is a bot which syncronises flair across several subreddits given any criteria provided. In the case of a Karma Sync, a special function has already been provided in run_examples.py which shows how this can be done. You can configure any number of subreddits to sync and can create any sync rules you want. All subreddits must obey the same synchronization rules, however.

## How does it work?

The bot requires a user that can access all subreddits in question. This user finds all flair differences between these subreddits, applies the rules you provide in the form of a custom function, and synchronises them in the way your rules function specifies. 

The input "syncfunc" is a user-defined function that takes as input a dictionary whose keys are subreddit names and whose values are a dictionary with 'text' and 'css_class' as keys. This represents the data for one user. The intent of the sync function is to return a similar dictionary keyed by subreddit but with the values being the final state for the user's flair on the subreddits. To assist in this, the syncfunc also takes a second parameter which is a list of all subreddit names, as some subreddits may not have flair data in them yet and will require new flair to be created.

The input "syncsubs" is a user-defined list of subreddits you wish to synchronise in addition to the one already provided to the bot. **There is no reason to add the subreddit that the bot already knows about to this list.** This list of subreddits must also have the assigned bot user as a moderator for the flair to synchronize. 

# Getting started

This guide assumes a Ubuntu 14.04 Linux machine with python 2.7 installed on it. 

1. sudo apt-get install git
2. sudo apt-get install sqlite3 libsqlite3-dev
3. cd <directory you wish to hold the bot>
4. git clone <url to this repository>
5. pip install -r requirements.txt

Now that it's installed, in order to run it you will need the following (assuming you own/mod the subreddit):

1. A user account which the bot will use. 
    * This account will write responses and assign karma flair. 
    * Ensure permissions are appropriate for that work.
    * Must have password
    * Must have a client_id and client_secret from here: https://www.reddit.com/prefs/apps
    * client_id and client_secret can be on one account, but you **must add the bot users as developers**
    * If you wish to use FKS, the user account must share moderator privileges with the other subreddits.
2. A run.py script. 
    * You may copy the run_example.py found in the code.
    * You may also create your own.
3. CSS classes for flair assignment
    * Mentioned above
    * root_css class
    * list of css_ignores classes
    * list of tiered flair classes and their karma thresholds

Place that info into your run.py

Next, copy the `responses/SUBREDDIT_EXMPL` directory to `responses/yoursubreddit` where "yoursubreddit" is the name of the subreddit you're using this bot on. Do this for each subreddit that's going to use the bot. You may got through the templates for the responses and modify them to your needs, but generic responses are in place and should be sufficient.

The last step is to run the code!

> nohup python run.py &

This will run the process in the background and assign karma to users as they come!

That's it! Any issues, file a ticket with this repository.

