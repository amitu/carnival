from django.test import TestCase
from django.test.client import Client

import json

from .models import Album, Photo, User

class AlbumListTestCase(TestCase):
	def setUp(self):
		john = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		a1 = Album.objects.create(name="Album 1", user=john)
		a2 = Album.objects.create(name="Album 2", user=john)
		Photo.objects.create(title="Photo 1", album=a1, url="http://i.imgur.com/zLvRB2Z.jpg")

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

	def testAlbumsPage404(self):
		c = Client()
		r = c.get("/john2/albums/")
		self.assertEqual(r.status_code, 404)
		self.assertEqual(r.templates[0].name, "404.html")
		self.assertEqual(len(r.templates), 1)

	# singluars vs plurals

	def testAlbumAPI(self):
		c = Client()
		r = c.get("/album/1/?json=true")
		self.assertEqual(r.status_code, 200)
		data = json.loads(r.content)
		self.assertEqual(len(data["photo_list"]), 1)
		self.assertEqual(data["pagination_info"]["hits"], 1)
		self.assertEqual(data["photo_list"][0]["title"], "Photo 1")

	def testAlbumAPI404(self):
		c = Client()
		r = c.get("/album/10/?json=true")
		self.assertEqual(r.status_code, 404)

	def testAlbumPage(self):
		c = Client()
		r = c.get("/album/1/")
		self.assertEqual(r.templates[0].name, "photo_list.html")
		self.assertEqual(len(r.templates), 1)

	def testAlbumPage404(self):
		c = Client()
		r = c.get("/album/10/")
		self.assertEqual(r.status_code, 404)
		self.assertEqual(r.templates[0].name, "404.html")
		self.assertEqual(len(r.templates), 1)
