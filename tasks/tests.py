from django.test import TestCase
from django.test.client import Client

import json

from .models import Task

class CreateUniquesTestCase(TestCase):
	def setUp(self):
		Task.objects.create_unique("foo")
		Task.objects.create_unique("foo")
		Task.objects.create_unique("foo2")

	def test(self):
		c = Client()
		r = c.get("/tasks/?secret=super secret")
		self.assertEqual(r.status_code, 200)
		data = json.loads(r.content)
		self.assertEqual(data["total_tasks"], 2)
		self.assertEqual(data["statuses"]["open"], 2)

