import praw


try:
	f_visited = open("visited_posts.txt", "r+")
	old_visited = f_visited.read().split(",")
	if len(old_visited) > 1:
		append_string = ","
	else:
		append_string = ""
except IOError:
	f_visited = open("visited_posts.txt", "w+")
	old_visited = []
	append_string = ""
new_visited = []

r = praw.Reddit('sleeptight')
subreddit = r.subreddit('nosleep')

for post in subreddit.top(time_filter='day', limit=3):
	if len(new_visited) < 3:
		if not post.id in old_visited:
			record = "{0}{1}".format(append_string, post.id)
			append_string = ","
			f_visited.write(record)
			submission = {'id': post.id,
						  'title': post.title,
						  'author': post.author,
						  'upvotes': post.ups,
						  'permalink': post.permalink}
			new_visited.append(submission)
	else:
		break

msg_subject = ""
msg_body = ""
if len(new_visited) == 1:
	msg_subject = "There is {0} new /r/nosleep story trending in the last 24 hours:".format(len(new_visited))
	print("There is {0} new /r/nosleep story trending in the last 24 hours:".format(len(new_visited)))
	for i, s in enumerate(new_visited):
		msg_body += "{0}.) {1} by: {2} ({3} upvotes)\n\n".format(i+1, s['title'], s['author'], s['upvotes'])
		msg_body += "{0}\n\n".format(s['permalink'])
		print("{0}.) {1} by: {2} ({3} upvotes)".format(i+1, s['title'], s['author'], s['upvotes']))
elif len(new_visited) > 1:
	msg_subject = "There are {0} new /r/nosleep stories trending in the last 24 hours:".format(len(new_visited))
	print("There are {0} new /r/nosleep stories trending in the last 24 hours:".format(len(new_visited)))
	for i, s in enumerate(new_visited):
		msg_body += "{0}.) {1} by: {2} ({3} upvotes)\n\n".format(i+1, s['title'], s['author'], s['upvotes'])
		msg_body += "{0}\n\n".format(s['permalink'])
		print("{0}.) {1} by: {2} ({3} upvotes)".format(i+1, s['title'], s['author'], s['upvotes']))
		print(s['permalink'])
else:
	msg_subject = "There are no new top 3 stories within the last 24 hours."
	msg_body += "There are no new top stories to read since the last time you checked.\n\nSleep easy!"
	print("There are no new top 3 stories within the last 24 hours.")

r.redditor('songbirdy').message(msg_subject, msg_body)