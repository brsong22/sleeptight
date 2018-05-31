import praw

r = praw.Reddit('sleeptight')

subreddit = r.subreddit('nosleep')

top_visited = []
new_visited = []


for post in subreddit.top(time_filter='day'):
	if len(new_visited) < 3:
		if not post.id in top_visited:
			top_visited.append(post.id)
			submission = {'id': post.id,
						  'title': post.title,
						  'author': post.author,
						  'upvotes': post.ups}
			new_visited.append(submission)
	else:
		break
print("These are the top 3 nosleep stories trending in the last day:")
for i, s in enumerate(new_visited):
	print(i+1,".) ", s['title']," by: ",s['author']," (",s['upvotes']," upvotes)")