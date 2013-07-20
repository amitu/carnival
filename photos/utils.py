import facebook, tempfile

def download_all_in(urls, folder): 
	pass

def create_collage(photo_urls):
	# download all photos to a folder
	tmp = tempfile.gettempdir()
	download_all_in(photo_urls, tmp)

	# https://scottlinux.com/2011/08/13/create-photo-collage-in-linux/
	# 
	# montage *.jpg -border 2x2 -background black +polaroid -resize 75% -geometry -60-60 -tile x6 final.jpg
	
	# other alternative: http://cs.colby.edu/courses/S09/cs151-labs/labs/lab06/

def post_photo_on_facebook(photo_url, message, tags, token):
	graph = facebook.GraphAPI(token)
	graph.put_photo(open(photo_file), message, tags=tags)