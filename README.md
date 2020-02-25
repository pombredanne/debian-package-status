# Debian Package Status

This Python-based web server displays information in an HTML inteface about 
Debian software packages.
It pulls package information from /var/lib/dpkg/status and serves up a 
website where the package information can be browsed.

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
* Make project easily deployable (Docker image?)
* Deploy on webserver
* Clean up Unit Tests for each module