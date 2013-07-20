from importd import d

d(DEBUG=True)

@d("/")
def idx(request):
	return d.HttpResponse("hey")
	
if __name__ == "__main__":
    d.main()