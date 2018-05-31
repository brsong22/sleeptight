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
						  'upvotes': post.ups}
			new_visited.append(submission)
	else:
		break
if len(new_visited) == 1:
	print("There is {0} new /r/nosleep story trending in the last 24 hours:".format(len(new_visited)))
	for i, s in enumerate(new_visited):
		print("{0}.) {1} by: {2} ({3} upvotes)".format(i+1, s['title'], s['author'], s['upvotes']))
elif len(new_visited) > 1:
	print("There are {0} new /r/nosleep stories trending in the last 24 hours:".format(len(new_visited)))
	for i, s in enumerate(new_visited):
		print("{0}.) {1} by: {2} ({3} upvotes)".format(i+1, s['title'], s['author'], s['upvotes']))
else:
	print("There are no new top 3 stories within the last 24 hours.")