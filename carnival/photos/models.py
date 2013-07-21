from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from . import utils

class Album(models.Model):
	name = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	twitter_search = models.CharField(max_length=100, blank=True)

	def __unicode__(self): 
		return "%(name)s by %(user)s [twitter_search=%(twitter_search)s]" % (
			self.__dict__
		)

	def toJSON(self):
		return {
			"id": self.id,
			"name": self.name,
			"user": self.user.username
		}

	def mail_owner_if_x00(self):
		pass

	def collage_and_fb_it(self, message=""):
		if not message:
			message = "Collage for %s" % self.name

		# see if owner has fb access token
		token = user.get_profile().facebook_token
		if not token: return

		# for each photo find tagged users
		fbuids = set()
		photos = []
		for photo in self.photos.order_by("-likes").limit(7):
			for tagged_user in photo.tagged:
				fbuid = tagged_user.get_profile().facebook_uid
				if fbuid: fbuids.add(fbuid)
			photos.append(photo.url)
		collage_file_name = utils.create_collage(photos)
		tags = [{"tag_uid": uid} for uid in fbuids]

		utils.post_photo_on_facebook(collage_file_name, message, tags, token)

class Photo(models.Model):
	url = models.URLField()
	title = models.CharField(max_length=200)
	album = models.ForeignKey(Album)
	tagged = models.ManyToManyField(User, through="Tag")
	created_on = models.DateTimeField(default=datetime.now)

	def __unicode__(self): return "%(title)s <- %(album)s" % self.__dict__

	def toJSON(self):
		return {
			"url": self.url,
			"title": self.title,
			"album": self.album.id
		}

class Tag(models.Model):
	user = models.ForeignKey(User)
	photo = models.ForeignKey(Photo)
	# tagged_by = models.ForeignKey(User) 	# this is not allowed :-(
	tagged_by = models.IntegerField() 		# userid
	x = models.IntegerField(default=0)
	y = models.IntegerField(default=0)

	# width and height are constant for each tag?

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	twitter_username = models.CharField(max_length=100, blank=True)
	twitter_key = models.CharField(max_length=100, blank=True)
	twitter_secret = models.CharField(max_length=100, blank=True)
	facebook_uid = models.CharField(max_length=100, blank=True)
	facebook_token = models.CharField(max_length=100, blank=True)
