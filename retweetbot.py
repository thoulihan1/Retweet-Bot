import tweepy, time
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config')

CONSUMER_KEY = parser.get('twitter', 'CONSUMER_KEY')
CONSUMER_SECRET = parser.get('twitter', 'CONSUMER_SECRET')
ACCESS_KEY = parser.get('twitter', 'ACCESS_KEY')
ACCESS_SECRET = parser.get('twitter', 'ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

keywords = ["rt to", "retweet to", "rt and win", "retweet and win", "retweet for", "rt for", "rt 4"]
haveToFollow_keywords = ["follow", "following"]
haveToFav_keywords = ["favorite", "favourite", "fav", "fave", "like"]
bannedwords = ["vote", "bot", "b0t"]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def is_user_bot_hunter(username):
        clean_username = username.replace("0", "o")
        clean_username = clean_username.lower()
        if 'bot' in clean_username or 'spot' in clean_username:
                return True
        else:
                return False

def retweet(tweet):
	if not tweet.retweeted:
		try:
			api.retweet(tweet.id)
			print(bcolors.OKGREEN + "Retweeted " + bcolors.ENDC + tweet.text)
			followIfNecessary(tweet)
		except Exception:
			pass
	favIfNecessary(tweet)

def favIfNecessary(tweet):
	for fav in haveToFav_keywords:
		if fav.lower() in tweet.text.lower() and not tweet.favorited:
			try:
				api.create_favorite(tweet.id)
				print(bcolors.FAIL + "Favourited - " + bcolors.ENDC+ tweet.text)
			except Exception:
				pass

def followIfNecessary(tweet):
	for follow in haveToFollow_keywords:
		if follow.lower() in tweet.text.lower():
			user_id = tweet.retweeted_status.user.id
			api.create_friendship(user_id)
			print(bcolors.OKBLUE + "Followed - " + bcolors.ENDC +"@"+ tweet.author.screen_name)

def search(twts):
        for tweet in twts:
                if not any(k in tweet.text.lower() for k in keywords) or any(k in tweet.text.lower() for k in bannedwords):
                        continue
                if is_user_bot_hunter(str(tweet.author.screen_name)) == False:
                       retweet(tweet)

def run():
        for key in ["RT to win", "retweet to win"]:
                print "\nSearching for tweets with '"+key+"'...\n"
                search(api.search(q=key))


if __name__ == '__main__':
        while True:
                run()
