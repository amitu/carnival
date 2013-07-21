#### importd - development branch

``` shell
$ git clone https://github.com/amitu/importd.git
$ git checkout development
$ sudo python setup.py develop
```

#### carnival

``` shell
$ git clone https://github.com/amitu/carnival.git
$ cd carnival
$ sudo python setup.py develop # should install rest of dependencies
$ python -m carnival.app test tasks
$ python -m carnival.app test photos
$ python -m carnival.app syncdb
$ python -m carnival.app # runs the server
```

From a different shell

``` shell
$ python -m carnival.worker foo # start a worker named foo
```

From yet another shell 

``` shell
$ python -m carnival.pusher # this guy pushes users for workers to handle
```

Visit http://localhost:8000.