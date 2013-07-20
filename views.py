from .models import Task
from django.db.models import Count
from datetime import datetime, timedelta
from importd import d

def idx(request):
	# show a summary of tasks

	# no regard to performace, this is purely internal/debugging
	# tool

	statuses = Task.objects.values('status').annotate(count=Count('status'))
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
		"overdue_tasks": overdue_tasks,
		"slow_tasks": slow_tasks
	})

def get(request):
	# worker trying to get a new task
	pass

def done(request):
	# worker saying task is done
	pass

def clear_slow(request):
	# maitenance helper, find all slow tasks, and 
	# mark them unassigned
	Task.clear_slow()
	