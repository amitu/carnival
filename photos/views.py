from importd import d

from .utils import object_list

from .models import Album, Photo, User

def albums_jsoner(context):
	return {
		"album_list": [
			album.toJSON()
			for album in context["album_list"]
		], 
		"pagination_info": context.get("pagination_info", {})
	}

@d("/<username:username>/albums/")
def albums(request, username):
	return object_list( 
		request, 
		queryset = Album.objects.filter(
			user=d.get_object_or_404(User, username=username)
			# user__username=username is also suffecient, but we want proper 
			# 404 if user does not exist, and we dont want to give 404 if there
			# are no albums, which is what ll happen if we use 
			# allow_empty=False
		),
		template_name = "album_list.html",
		template_object_name = "album", 
		paginate_by = 10,
		jsoner = albums_jsoner
	)

def photo_jsoner(context):
	return {
		"photo_list": [
			photo.toJSON()
			for photo in context["photo_list"]
		],
		"album": context["album"].toJSON(),
		"pagination_info": context.get("pagination_info", {})
	}

@d("/album/<int:albumid>")
def album(request, albumid):
	return object_list( 
		request, 
		queryset = Photo.objects.filter(album__id=albumid),
		template_name = "photo_list.html",
		template_object_name = "photo", 
		paginate_by = 10,		
		extra_context = {
			"album": d.get_object_or_404(Album, pk=albumid)
		},
		jsoner = photo_jsoner
	)
