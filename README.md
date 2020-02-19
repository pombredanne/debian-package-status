# Debian Package Status

This Python-based web server displays information in an HTML inteface about 
Debian software packages.
It pulls package information from /var/lib/dpkg/status and serves up a 
website where the package information can be browsed.

## TO-DO

* <strike> Build Python web server </strike>
* <strike> Parse [debian control file](https://www.debian.org/doc/debian-policy/ch-controlfields.html) (/var/lib/dpkg/status). </strike>
* <strike> Display index page with list of packages alphabetically </strike>
* When clicking on links, dynamically convert parsed data to new HTML page (Alternatively, generate pages upfront for every package)
* Improve user experience with minimal but appealing CSS
* Make project easily deployable (Docker image?)
* Deploy on webserver
* Create HTML validation function