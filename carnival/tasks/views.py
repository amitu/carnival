from .models import Task
from django.db.models import Count
from datetime import datetime, timedelta
from importd import d

@d("/tasks/")
def idx(request):
	assert request.GET.get("secret") == "super secret"
	# show a summary of tasks

	# no regard to performace, this is purely internal/debugging
	# tool

	statuses = dict(
		(row["status"], row["count"]) for row in Task.objects.values(
			'status'
		).annotate(count=Count('status'))
	)
	total_tasks = sum(statuses.values())

	# tasks that are pending since more than k mins to be assigned, get k from
	# request.GET, default to 5

	now = datetime.now()
	k_mins_ago = now - timedelta(minutes=int(request.GET.get("k", 5)))

	overdue_tasks = Task.objects.filter(status="open").filter(
		created_on__lt=k_mins_ago
	).count()

	# slow workers

	slow_tasks = Task.objects.filter(status="assigned").filter(
		assigned_on__lt=k_mins_ago
	).count()

	return d.JSONResponse({
		"statuses": statuses,
		"total_tasks": total_tasks,
		"overdue_tasks": overdue_tasks,
		"slow_tasks": slow_tasks
	})

@d("/tasks/get/")
def get(request):
	# worker trying to get a new task
	assert request.REQUEST.get("secret") == "supersecret"
	return Task.objects.get(request.REQUEST["workername"])

@d("/tasks/mark-done/")
def mark_done(request):
	# worker saying task is done
	assert request.REQUEST.get("secret") == "supersecret"
	return Task.objects.mark_done(
		request.REQUEST["taskid"], request.REQUEST["assign_code"]
	)

@d("/tasks/clear-slow/")
def clear_slow(request):
	# maitenance helper, find all slow tasks, and 
	# mark them unassigned
	assert request.POST.get("secret") == "superdupersecret"
	Task.clear_slow()
	