##########
Change Log
##########

1.0.0 [22/03/2021]
******************
New
---
* Make the client generic to uses other that quantum chemistry


0.3.0 [22/02/2021]
******************

Changed
-------
* Make library more generic by removing references to the smiles (#26)

New
---
* Accept jobs as a list of JSON objects (#26)

0.2.0 [Unreleased]
******************

Added
-----
* Command to manage the jobs status
* Allow to pass the input via the command line (#10)
* Allow to retrieve the available collections (#13)
* Authentication functionality (#18)

Changed
-------
* Make input file optional (#10)
* Choose automatically the new collection name when adding jobs (#8)


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

