from django.test import TestCase
from django.test.client import Client

import json

from .models import Album, Photo, User

class AlbumListTestCase(TestCase):
	def setUp(self):
		john = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		Album.objects.create(name="Album 1", user=john)
		Album.objects.create(name="Album 2", user=john)

	def testAlbumsAPI(self):
		c = Client()
		r = c.get("/john/albums/?json=true")
		self.assertEqual(r.status_code, 200)
		data = json.loads(r.content)
		self.assertEqual(len(data["album_list"]), 2)
		self.assertEqual(data["pagination_info"]["hits"], 2)
		self.assertEqual(data["album_list"][0]["name"], "Album 1")

	def testAlbumsAPI404(self):
		c = Client()
		r = c.get("/john2/albums/?json=true")
		self.assertEqual(r.status_code, 404)

	def testAlbumsPage(self):
		c = Client()
		r = c.get("/john/albums/")
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.templates[0].name, "album_list.html")
		self.assertEqual(len(r.templates), 1)
