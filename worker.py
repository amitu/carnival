import sys, requests, time

worker_name = sys.argv[1]
task_server = "http://localhost:8000/tasks/"

def get_task():
	r = requests.get(task_server + "get/", {"worker_name": worker_name})
	return r.json()

def mark_done(taskid, assign_code):
	r = requests.post(
		task_server + "get/", {
			"worker_name": worker_name, "taskid": taskid,
			"assign_code": assign_code
		}
	)
	return r.json()

def do_once():
	task = get_task()

	if not task: return # server returns empty dict if there is no task

	# what to do??? task["data"] contains userid

	# for user find twitter username
	# find latest tweets by user
	# find all urls in the tweet
	# find mimetype of each url, if it is imagish, or is imagur then collect it
	# for each url see if its already there in db, if not create a picture

	# once done, see the count of photos in album, if its x00 then send a mail

	mark_done(task["taskid"], task["assign_code"])

def main():
	while True:
		try:
			do_once()
			time.sleep(1) # grow enough that this line has to be removed!
		except KeyboardInterrupt:
			print "Worker stopped."
			break
		except Exception, e:
			print "Exception while doing the task", e

if __name__ == "__main__":
	main()
