import praw

class sleeptight_bot:

	def __init__(self):

		self.sub = 'nosleep'
		self.bot_name = 'sleeptight'
		self.bot = praw.Reddit(self.bot_name)
		self.subreddit = self.bot.subreddit(self.sub)

		self.new_visited = []

		try:
			self.f_visited = open("visited_posts.txt", "r+")
			self.old_visited = self.f_visited.read().split(",")
			if len(self.old_visited) > 1:
				self.prepend_string = ","
			else:
				self.prepend_string = ""
		except IOError:
			self.f_visited = open("visited_posts.txt", "w+")
			self.old_visited = []
			self.prepend_string = ""

	def get_top_posts_day(self, top_x):
		for post in self.subreddit.top(time_filter='day', limit=top_x):
			if len(self.new_visited) < top_x:
				if not post.id in self.old_visited:
					self.f_visited.write("{0}{1}".format(self.prepend_string, post.id))
					prepend_string = ","
					submission = {'id': post.id,
								  'title': post.title,
								  'author': post.author,
								  'upvotes': post.ups,
								  'permalink': post.permalink}
					self.new_visited.append(submission)
			else:
				break

	def send_reddit_pm(self, username):
		msg_subject = ""
		msg_body = ""
		if len(self.new_visited) == 1:
			msg_subject = "There is {0} new /r/nosleep story trending in the last 24 hours:".format(len(self.new_visited))
			for i, s in enumerate(self.new_visited):
				msg_body += "{0}.) {1} by: {2} ({3} upvotes)\n\n".format(i+1, s['title'], s['author'], s['upvotes'])
				msg_body += "{0}\n\n".format(s['permalink'])
		elif len(self.new_visited) > 1:
			msg_subject = "There are {0} new /r/nosleep stories trending in the last 24 hours:".format(len(self.new_visited))
			for i, s in enumerate(self.new_visited):
				msg_body += "{0}.) {1} by: {2} ({3} upvotes)\n\n".format(i+1, s['title'], s['author'], s['upvotes'])
				msg_body += "{0}\n\n".format(s['permalink'])
		else:
			msg_subject = "There are no new top stories within the last 24 hours."
			msg_body += "There are no new top stories to read since the last time you checked.\n\nSleep easy!"
		self.bot.redditor(username).message(msg_subject, msg_body)


nosleep = sleeptight_bot()
nosleep.get_top_posts_day(3)
nosleep.send_reddit_pm('songbirdy')