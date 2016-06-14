# reddit-bot

Bot which automatically scans user comments and awards karma when other users indicate they'd like to give them some karma. Updates their user flair to display this karma. Has multiple tiers of Karma flair.

## How does it work?

The bot scans the last 200 comments and looks for a comment that says "+karma". When it sees this comment, it assigns Karma to the assigned user and updates the user's karma. This follows the rules in the UserKarmaGuide.md file. There are an arbitrary number of karma tiers available, and you can assign any CSS class you wish to that. 

There's a root_css class. This is given to any user assigned karma. It's the basic class for adding karma.

ex: "green"

There's also a list of css_ignores. If the bot sees that a person has one of these classes, their karma will not be updated. This is good for moderators and those who have been warned or blacklisted.

ex: ["red", "mod"]

There's also a list of bonus_css classes. This is a list of tuples of size 2. The first tuple is the name of the bonus class with special flair design, and the second is the threshold in which this flair will be assigned. In the below example, css class "tier3" is assigned at 50+ karma, and "tier5" is assigned at 250+ karma. 

ex: [("tier2", 15),("tier3", 50),("tier4", 100),("tier5",250),("tier6",500)]

The bot may run on as many subreddits as you like simultaneously. 

## Getting started

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

## Note

Whenever you restart the bot, you must also delete the existing database for the subreddits. These can be found in the `db/` folder.

Another note, it is known that when you restart the bot, double karma will be assigned. This is because we must remove the existing databases. It is a bug, but one that is not fixed yet. 

# Bugs / TODO

1. Graceful shut down and restart, preventing the issue in the Note above from occuring.
2. Per-bot configs, allowing for automatic pickup of new subreddits (removing the need for a restart)
