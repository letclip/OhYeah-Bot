# import the modules 
import praw
import time
import os

CRITERIA = ["Oh no", "oh no", "OH NO", "oh no!", "OH NO!"]
REPLY_TEMPLATE = "[OHHHH YEAAAAHHH!!](https://youtu.be/rLRitISbqng?t=13)"

#import logging   # Logging

#handler = logging.StreamHandler()
#handler.setLevel(logging.DEBUG)
#for logger_name in ("praw", "prawcore"):
#    logger = logging.getLogger(logger_name)      <<< Logging, useful for debugging any issues, but not needed now so commented out.
#    logger.setLevel(logging.DEBUG)
#    logger.addHandler(handler)


def bot_login(): # Logs the bot into reddit

    # initialize with appropriate values
    client_id = "" 
    client_secret = "" 
    username = "" 
    password = "" 
    user_agent = "" 


    # creating an authorized instance 
    print ("Logging in....")
    r = praw.Reddit(client_id = client_id,  
                         client_secret = client_secret,  
                         username = username,  
                         password = password, 
                         user_agent = user_agent) 
    print ("Logged in")
    return r
    

def inboxcheck():
	# Sort inbox, then act on it
    # Invert the inbox so we're processing oldest first
	for item in reversed(list(r.inbox.unread(limit=None))): # Sorts messages oldest to newest
		if item.author is None: 
			item.mark_read()
			continue

		if 'blacklist me' in item.body:
			item.mark_read() # Marks message as read so it is not read again by the bot
			blacklist.append(message.author)

			messsage.reply("You have been added to the blacklist :)")
			if not os.path.isfile("blacklist.txt"):
				blacklist = []
			else:
				with open("blacklist.txt", "r") as e:
					blacklist = e.read()
					blacklist = blacklist.split("\n")
					blacklist = list(filter(None, blacklist))

			return blacklist


def run(r, comments_replied_to, inboxcheck):
	print ("Searching 1,000 comments")


	for comment in r.subreddit('popular').comments(limit=1000): # Scans comments
		for i in CRITERIA:	# Checks them against the criteria i've set above.
			if i in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me and comment.author not in blacklist(): # Checks if the bot has already replied to the comment, and if the comment is from the bot or not.
				print ("Found Comment: \n" + "ID: " + comment.id + "\nTEXT:" + comment.body + "\nAUTHOR:" + str(comment.author))
				comment.reply(REPLY_TEMPLATE) # Replies
				print ("Bot replied to: " + comment.id)

				comments_replied_to.append(comment.id)

				with open ("comments_replied_to.txt", "a") as f:   # Writes the comment id in a file to keep note of.
					f.write(comment.id + "\n")
				#print("Sleeping for 15 minutes after replying to avoid rate limiting.")
				#time.sleep(900) # To avoid rate limiting as the bot has no karma, can't comment more than once every 15 or so minutes.

	print ("Search Completed.")

	#print (comments_replied_to) - Prints out the ID of all the comments that have been replied to, but i don't really want this spamming the console, it could be useful for debugging.

	print("Checking inbox")
	inboxcheck()

	print ("Sleeping for 15 seconds...")
	time.sleep(15)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:        
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
#print (comments_replied_to)

while True:
	run(r, comments_replied_to, inboxcheck)



	# TODO
	# Add a blacklist function, so people can send the bot a PM and it will no longer reply to their messages ever
	# Add a cleanup function, delete own comments with -5 reputation or less
	# Be a little smarter with what to reply to

