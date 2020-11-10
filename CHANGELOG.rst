##########
Change Log
##########

0.2.0 [Unreleased]
******************

Added
-----
* Command to manage the jobs status

Changed
-------
* Make input file optional (#10)
* Allow to pass the input via the command line (#10)

  Changed
-------
* Running jobs must include username (#9)

0.1.0 [03/11/2020]
******************

Added
-----

* Interface to web service using `add`, `query`, `compute` or `report` actions (#1)
* Interface to [Openstack Swift](https://docs.openstack.org/swift/latest/) to store large objects
* Allow to query jobs based on their size (#4)
* Allow to report either in CSV or JSON format.

