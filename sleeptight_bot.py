import praw

class sleeptight_bot:

	def __init__(self):

		self.__sub = 'nosleep'
		self.__bot_name = 'sleeptight'
		self.__bot = praw.Reddit(self.__bot_name)
		self.__subreddit = self.__bot.subreddit(self.__sub)

		self.__f_old_stories = self.__f_get_read_stories()
		self.__old_stories = self.__f_old_stories.read().split(",")
		self.__stories_delim = "" if self.__old_stories[0] == '' else ","
		self.__new_stories = []

		self.__f_bot_subs = self.__f_get_subscribers()
		self.__bot_subs = self.__f_bot_subs.read().split(",")
		self.__subs_delim = "" if self.__bot_subs[0] == '' else ","

		self.__get_new_subscribers()

			

	def get_top_posts_day(self, top_x):
		for post in self.__subreddit.top(time_filter='day', limit=top_x):
			if len(self.__new_stories) < top_x:
				if not post.id in self.__old_stories:
					submission = {'id': post.id,
								  'title': post.title,
								  'author': post.author,
								  'upvotes': post.ups,
								  'permalink': post.permalink}
					self.__new_stories.append(submission)
			else:
				break
		if len(self.__new_stories) > 0:
			self.__save_new_stories()

	def send_reddit_pm(self, username):
		msg_subject = ""
		msg_body = ""
		if len(self.__new_stories) == 1:
			msg_subject = "There is {0} new /r/nosleep story trending in the last 24 hours:".format(len(self.__new_stories))
			for i, s in enumerate(self.__new_stories):
				msg_body += "{0}.) {1} by: {2} ({3} upvotes)\n\n".format(i+1, s['title'], s['author'], s['upvotes'])
				msg_body += "{0}\n\n".format(s['permalink'])
		elif len(self.__new_stories) > 1:
			msg_subject = "There are {0} new /r/nosleep stories trending in the last 24 hours:".format(len(self.__new_stories))
			for i, s in enumerate(self.__new_stories):
				msg_body += "{0}.) {1} by: {2} ({3} upvotes)\n\n".format(i+1, s['title'], s['author'], s['upvotes'])
				msg_body += "{0}\n\n".format(s['permalink'])
		else:
			msg_subject = "There are no new top stories within the last 24 hours."
			msg_body += "There are no new top stories to read since the last time you checked.\n\nSleep easy!"
		self.__bot.redditor(username).message(msg_subject, msg_body)

	def __f_get_read_stories(self):
		try:
			f_old_stories_stories = open("visited_posts.txt", "r+")
		except IOError:
			f_old_stories_stories = open("visited_posts.txt", "w+")
		return f_old_stories_stories

	def __save_new_stories(self):
		stories = ",".join([s['id'] for s in self.__new_stories])
		self.__f_old_stories.write("{0}{1}".format(self.__stories_delim, stories))

	def __f_get_subscribers(self):
		try:
			f_bot_subs = open("sleeptightbot_subs.txt", "r+")
		except IOError:
			f_bot_subs = open("sleeptightbot_subs.txt", "w+")
		return f_bot_subs
		# unread_messages = self.__bot.inbox.unread(limit=None)
		# for msg in unread_messages:
		# 	print(msg.author)

	def __get_new_subscribers(self):
		unread_messages = self.__bot.inbox.unread(limit=None)
		# new_subs = []
		# for msg in unread_messages:
		# 	if msg.subject == "subscribe" and not msg.author in self.__bot_subs:
		# 		self.__bot_subs += msg.author
		# sub_list = 



		
nosleep = sleeptight_bot()
nosleep.get_top_posts_day(3)
nosleep.send_reddit_pm('songbirdy')