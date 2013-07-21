from django.db import models
from datetime import datetime

class TaskManager(models.Manager):
	def clear_slow(self):
		pass

	def add_task(data):
		# if data is already there and is not marked done only
		# then add it.
		pass

class Task(models.Model): # unique data task.
	data = models.TextField()
	status = models.CharField(max_length=20, default="open") # open/assigned/done
	assign_code = models.CharField(max_length=32, blank=True)

	created_on = models.DateTimeField(default=datetime.now)
	assigned_on = models.DateTimeField(null=True)
	done_on = models.DateTimeField(null=True)

	objects = TaskManager()

	def assign(self, workername="unknow"):
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
