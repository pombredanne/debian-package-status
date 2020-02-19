# Debian Package Status

This Python-based web server displays information in an HTML inteface about 
Debian software packages.
It pulls package information from /var/lib/dpkg/status and serves up a 
website where the package information can be browsed.

## TO-DO

* ~~Build Python web server~~
* ~~Parse /var/lib/dpkg/status file~~
    * ~~See [debian control file sytax](https://www.debian.org/doc/debian-policy/ch-controlfields.html)~~
* ~~Display index page with list of packages alphabetically~~
* When clicking on links, dynamically convert parsed data to new HTML page (Alternatively, generate pages upfront for every package)
* Improve user experience with minimal but appealing CSS
* Make project easily deployable (Docker image?)
* Deploy on webserver
* Create HTML validation function