# Debian Package Status

This Python-based web server displays information in an HTML inteface about 
Debian/Ubuntu software packages.
It pulls package information from /var/lib/dpkg/status and serves up a 
website where the package information can be browsed.

It contains no external dependencies and only relies on the Python 3.6 Standard Library.

An example is currently hosted on Heroku: https://warm-earth-66720.herokuapp.com/

## Getting Started

### Prerequisites
This project requires Python 3.6 or above. It only uses the Python Standard Library and therefore does not depend on any external modules.

You can check your installed Python version with:
```
$ python --version
```

### Running the server (localhost)
You can run the server locally by executing server.py. By default, the server executes on localhost port 80 and serves the included status.real dpkg/status file.
```
$ python server.py
Initializing web server with the following parameters:
ip_address: localhost
port: 80
dpkg_status_filepath: status.real
```
Navigate to [localhost:80](http://localhost:80) in your webbrowser to access the web server.

### Runing the server (local network)

You can run the server on the local network by specifying 0.0.0.0 as the IP address and port 80. This will make the server available on port 80 for all IP addresses that your computer is assigned.
```
$ python server.py -i 0.0.0.0 -p 80
```

Hint: You can check your computer's IP address with ```$ ipconfig``` on Windows or ```$ ifconfig``` on Linux.

## Getting Help
You can see the available command line options by providing the --help flag to the server.
```
$ python server.py --help
optional arguments:
  -h, --help            show this help message and exit
  -i IPADDRESS, --ipaddress IPADDRESS
                        IP address of the server (localhost by default).
  -p PORT, --port PORT  Port that server should serve (80 by default).
  -f FILE, --file FILE  Filepath to dpkg status file (usually
                        /var/lib/dpkg/status). By default status.real is used.
```

## Deployment on Heroku
Heroku is a container-based cloud Platform as a Service (Paas). They provide a free tier that allows users 550 free 'dyno' hours per month (1000 if credit card verified). When the server does not receive traffic for 30 minutes, the process will go to 'sleep' which will save 'dyno' hours. It will then take 5-10 seconds to 'wake' the server when a new request is received.

To deploy the web server on Heroku, first create a Heroku account https://signup.heroku.com/.

[Install Heroku command line interface (CLI)](https://devcenter.heroku.com/articles/heroku-cli#download-and-install]).

Login to Heroku from command line
```
$ heroku login
```

Navigate to the root of the debian-package-status project and [create a heroku app](https://devcenter.heroku.com/articles/creating-apps). A random name will be given to the app if one is not specified (you can always [rename the app later](https://devcenter.heroku.com/articles/renaming-apps)).
```
$ heroku create
Creating app... done, ⬢ warm-earth-66720
https://warm-earth-66720.herokuapp.com/ | https://git.heroku.com/warm-earth-66720.git
```

You can make changes to the source code and push the changes to Heroku using git.
```
$ git push heroku master
Counting objects: 4, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 402 bytes | 402.00 KiB/s, done.
Total 4 (delta 2), reused 0 (delta 0)
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Python app detected
remote: -----> Need to update SQLite3, clearing cache
remote: -----> Installing python-3.6.10
remote: -----> Installing pip
remote: -----> Installing SQLite3
remote: Sqlite3 successfully installed.
remote: -----> Installing requirements with pip
remote:
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote:
remote: -----> Compressing...
remote:        Done: 44M
remote: -----> Launching...
remote:        Released v5
remote:        https://warm-earth-66720.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/warm-earth-66720.git
   ef0edd2..a35d740  master -> master
```

Note: Heroku uses the ```Procfile``` to know which script to execute and what parameters to pass. The Heroku app environment has ```$PORT``` environment variable which should be passed into server.py. ```requirments.txt``` is empy because there are no dependencies for this project, but the file must still exist so that Heroku recognizes the app as a Python app.


## TO-DO

* <strike> Build Python web server </strike>
* <strike> Parse [debian control file](https://www.debian.org/doc/debian-policy/ch-controlfields.html) (/var/lib/dpkg/status). </strike>
* <strike> Display index page with list of packages alphabetically </strike>
* <strike> When clicking on links, dynamically convert parsed data to new HTML page (Alternatively, generate pages upfront for every package) </strike>
    * <strike> Display Name </strike>
    * <strike> Display Description </strike> Parse description newlines
    * <strike> Display Package dependencies, ignoring versions </strike>
    * <strike> Reverse dependencies (requires building a graph) </strike>
    * <strike> Only link dependecies that exist in the list of packages (Don't allow broken links to non-installed pacakges) </strike>
* <strike> Improve user experience with minimal but appealing CSS </strike>
* <strike> Implement command line arguments </strike>
* <strike> Make project easily deployable </strike>
* <strike> Deploy on webserver </strike>
* Clean up Unit Tests for each module
