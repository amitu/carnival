from carnival import app

import time

from tasks.models import Task
from photos.models import UserProfile

def do_once():
	for profile in UserProfile.objects.all():
		Task.objects.create_unique(profile.user_id)

def main():
	while True:
		try:
			do_once()
			print "Pushed once, going to sleep for 20 mins."
			time.sleep(20 * 60) # 20 mins
			print "Woke up."
		except KeyboardInterrupt:
			print "Puser stopped."
			break
		except Exception, e:
			print "Exception while pushing", e

if __name__ == "__main__":
	main()
