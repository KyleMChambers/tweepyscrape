#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "0NUWdrZ3bSCRbolngziMJBR9e"
consumer_secret = "No14MaB8cXmUhgZPRNJZyyi2RQneK4C3PWTSZeSqFhzHJdvhgZ"
access_key = "1230297252553424897-tpJiBoOHYMBj0qRMLB0ke8JKBgu4j0"
access_secret = "6XSngtX95JquwnDD0pT6aYAofFHkDsMVHRkccDNOEPFYI"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		#print "getting tweets before %s" % (oldest)
		print("getting tweets before %s" % (oldest))

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)


		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print("...%s tweets downloaded so far" % (len(alltweets)))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.replace('\n',' '), tweet.retweet_count, tweet.favorite_count, tweet.retweeted] for tweet in alltweets]
	#for tweet in alltweets:
		# if (not tweet.retweeted) and ('RT @' not in tweet.text):
		#if ('RT @' not in tweet[2]):
	#write the csv
	# with open('%s_tweets.csv' % screen_name, 'w', encoding='utf-8') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(["id","created_at","text", "retweet_count", "favorite_count", "retweeted"])
	# 	writer.writerows(outtweets)

	#remove retweets and export to csv
	with open('%s_tweets.csv' % screen_name, 'w', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text", "retweet_count", "favorite_count", "retweeted"])
		for tweet in outtweets:
			if ('RT @' not in tweet[2]):
				writer.writerow(tweet)
	pass

if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("KanyeWest")
