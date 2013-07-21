from importd import d

d(
	DEBUG=True,
	INSTALLED_APPS=[
		"django.contrib.contenttypes",
		"django.contrib.auth",

		"photos", 
		"tasks",
	]
)
	
if __name__ == "__main__":
    d.main()