from django.db import models
from datetime import datetime

class TaskManager(models.Manager):
	def clear_slow(self):
		pass

	def create_unique(self, data):
		if self.filter(data=data).exclude(status="done").count(): return
		return super(TaskManager, self).create(data=data)

	def get_lock(self): pass
	def release_lock(self): pass

	def get(self, workername):
		# this method should be locked. if we use mysql we can use get_lock()
		# for that, http://djangosnippets.org/snippets/2443/
		# 
		# or we can explore the possibility of transactions if database setup 
		# allows.
		# 
		# our current server is single threaded so no locking is required

		self.get_lock()
		try:
			tasks = list(self.filter(status="open").limit(1))
			if not tasks: return {}
			task = tasks[0]
			task.assign(workername)
			return {
				"data": task.data,
				"assign_code": task.assign_code,
				"id": task.id
			}
		finally:
			self.release_lock()

	def mark_done(self, taskid, code):
		self.get_lock()
		try:
			task = self.get(id=taskid)
			task.mark_done(code)
			return {"success": "true"}
		finally:
			self.release_lock()

class Task(models.Model): # unique data task.
	data = models.TextField()
	status = models.CharField(max_length=20, default="open") # open/assigned/done
	assign_code = models.CharField(max_length=32, blank=True)

	created_on = models.DateTimeField(default=datetime.now)
	assigned_on = models.DateTimeField(null=True)
	done_on = models.DateTimeField(null=True)

	objects = TaskManager()

	def assign(self, workername="unknown"):
		assert self.status == "open"
		now = datetime.now()

		key = "%s:%s:%s" % (workername, self.data, now)
		assign_code = "%s:%s" % (workername, md5.new(key))[:32]

		self.assigned_on = now
		self.status = "assigned"
		self.assign_code = assign_code
		self.save()

		return assign_code

	def mark_done(self, assign_code):
		assert self.assign_code == assign_code
		assert self.status == "assigned"

		self.status = "done"
		self.done_on = datetime.now()
		# leaving assign_code in, so workername related data can
		# be found
		self.save()
