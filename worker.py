import sys, requests, time, tweepy, re
from django.core.mail import EmailMessage

worker_name = sys.argv[1]
task_server = "http://localhost:8000/tasks/"
word_split_re = re.compile(r'(\s+)')
simple_url_re = re.compile(r'^https?://\[?\w', re.IGNORECASE)
simple_url_2_re = re.compile(r'^www\.|^(?!http)\w[^@]+\.(com|edu|gov|int|mil|net|org)$', re.IGNORECASE)
TRAILING_PUNCTUATION = ['.', ',', ':', ';', '.)']
WRAPPING_PUNCTUATION = [('(', ')'), ('<', '>'), ('[', ']'), ('&lt;', '&gt;')]

def get_task():
	r = requests.get(task_server + "get/", {"worker_name": worker_name})
	return r.json()

def mark_done(taskid, assign_code):
	r = requests.post(
		task_server + "mark-done/", {
			"worker_name": worker_name, "taskid": taskid,
			"assign_code": assign_code
		}
	)
	return r.json()

def get_urls_from_text(text):
	# https://github.com/django/django/blob/master/django/utils/html.py#L196
    words = word_split_re.split(text)
    urls = set()

    for i, word in enumerate(words):
        match = None
        if '.' in word or '@' in word or ':' in word:
            # Deal with punctuation.
            lead, middle, trail = '', word, ''
            for punctuation in TRAILING_PUNCTUATION:
                if middle.endswith(punctuation):
                    middle = middle[:-len(punctuation)]
                    trail = punctuation + trail
            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead = lead + opening
                # Keep parentheses at the end only if they're balanced.
                if (middle.endswith(closing)
                    and middle.count(closing) == middle.count(opening) + 1):
                    middle = middle[:-len(closing)]
                    trail = closing + trail

            # Make URL we want to point to.
            url = None
            nofollow_attr = ' rel="nofollow"' if nofollow else ''
            if simple_url_re.match(middle):
                url = smart_urlquote(middle)
            elif simple_url_2_re.match(middle):
                url = smart_urlquote('http://%s' % middle)
            urls.add(url)
    return urls

def get_api_for_user(user):
	# for user find twitter username
	twitter_username = user.getProfile().twitter_username
	user_key = user.getProfile().twitter_key
	user_secret = user.getProfile().twitter_secret

	auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
	auth.set_access_token(user_key, user_secret)
	api = tweepy.API(auth)
	return api

def get_urls_from_tweets(api):
	# find latest tweets by user
	urls = []
	return urls

def get_imagish_urls(urls):
	# find mimetype of each url?

	return [
		url for urls 
		if 
			url.lower().endswith(".jpg") or 
			url.lower().endswith(".jpeg") or
			url.lower().endswith(".png") or
			url.lower().endswith(".gif")
	]

def get_user_albums_with_tweet_search(user):
	albums = Album.objects.filter(user=user).exclude(twitter_search__eq="")
	if not albums:
		albums = [
			Album.objects.create(
				user=user, title="#carnival", twitter_search="#carnival"
			)
		]
	return albums

def get_new_images(tweet_images, album):
	# using brute force, one query per url approach to begin with
	new_images = []
	for image in tweet_images:
		if Photo.objects.filter(album=album).filter(url=url).count():
			continue
		new_images.append(image)
	return new_images

def insert_images(album, images, tweet):
	for image in images:
		Photo.objects.create(url=image, album=album, title=tweet)

def send_mail_about_album(album):
	album_centuary = album.photo_set.count() // 100
	if album_centuary > 5: return
	EmailMessage(
		subject = "%s has %s photos!" % (
			album.twitter_search, album_centuary * 100
		),
		body = "I am awesome", 
		from_email = "Website Host <hashtag@website.com>",
		to = [album.user.email], 
		bcc = ["sd@website.com"], 
	).send()

def do_once():
	task = get_task()

	if not task: return # server returns empty dict if there is no task

	user = User.objects.get(id=task["data"])
	albums = get_user_albums_with_tweet_search(user)

	api = get_api_for_user(user)

	tweets = api.user_timeline(count=100)

	for album in albums:
		before_album_centuary = album.photo_set.count() // 100
		for tweet in tweets:
			if album.twitter_search not in tweet.text: continue
			# find all urls in the tweet.text
			tweet_urls = get_urls_from_text(tweet.text)
			tweet_images = get_imagish_urls(tweet_urls)
			new_images = get_new_images(tweet_images, album)
			insert_images(album, new_images, tweet.text)

		# once done, see the count of photos in album, if its x00 then send a mail
		after_album_centuary = album.photo_set.count() // 100

		if after_album_centuary != before_album_centuary:
			send_mail_about_album(album)

	mark_done(task["taskid"], task["assign_code"])

def main():
	while True:
		try:
			do_once()
			time.sleep(1) # grow enough that this line has to be removed!
		except KeyboardInterrupt:before_album_centuary = album.photo_set.count() // 100
			print "Worker stopped."
			break
		except Exception, e:
			print "Exception while doing the task", e

if __name__ == "__main__":
	main()
