from importd import d

d(
	DEBUG = True,
	INSTALLED_APPS = [
		"django.contrib.contenttypes",
		"django.contrib.auth",

		"carnival.photos", 
		"carnival.tasks",
	],
	TWITTER_KEY = "...", 
	TWITTER_SECRET = "...",
	AUTH_PROFILE_MODULE = 'carnival.photos.models.UserProfile',
)
	
if __name__ == "__main__":
    d.main()