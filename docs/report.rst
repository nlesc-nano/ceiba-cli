
Report
======
The ``report`` command send the results of the jobs computed by the user to
the web service. You can also send "standalone" data to the server. Where standalone
means data that is not associated to a job in the server, for example because it
has been previously computed.

To report the results you need to type in the terminal:
::

   moka compute

Or if you want to have more control over what is reported you can provide an input file like:
::

   moka compute input_report.yml

Where the *input_compute.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`report input` metadata.

.. _report input:

Report Input File
*****************
The input file contains the following mandatory keywords:

::

   # URL to the insilico server
   url:
      http://localhost:8080/graphql

   # Path to the Folder where the jobs run (default "workdir_moka")
   path_results: "path/to/workdir"

There are also the following optional keywords:

::

   # Pattern to search for the result files (default "results*csv")
   output: "results*csv"

   # Pattern to search for the input files (default "inputs*json")
   input: "inputs*json"

   # Pattern to search for the optimized molecular geometry
   geometry: "geometry*xyz"

   # The data to report is not associated to a job (default False)
   is_standalone: True

   # If the data is already in server you can either:
   # KEEP the old data
   # OVERWRITE and discard the old data
   # MERGE the new and the old data
   # APPEND new data at the end of the old data array
   # Default = KEEP
   duplication_policy: "KEEP"

Check the :ref:`large objects data storage` for further information on
saving large output files.

.. _job metadata:

How does it work?
*****************
The library enters the ``path_results`` and search recursively all the files and
directories name like ``job_*``. In each subfolder, apart from the
computed data (specificied with the ``pattern`` keyword), the ``report`` command
would try to collect the metadata associated with the job in a files named
*metadata.yml* containing the following information:
::

   job_id: 1271269411
   property:
       collection_name: awesome_data
       smile: CC(=O)O
       smile_id: 76950

*Without the metadata no data is reported back to the server*.

.. _large objects data storage:

Large objects data storage
**************************
For many simulation it is desirable to store the output plain data and/or the binary checkpoints.
Those files can be used to retrieve data that is not available in the database or to restart
a calculation to perform further computations.

Those large objects are not suitable for storage in a database but fortunately there are
technologies like `swift openstack <https://docs.openstack.org/swift/latest/>`_ that allows
to store these kind of data in an efficient and safely way.



In order to storage large output you need to provide in the yaml file the following keywords:
::

     large_objects:
       # URL to the datastorage service
       url: "http://large_scientific_data_storage.pi"
       # The large file(s) to search for
       patterns:  ["output*hdf5"]
       

.. Note::
   * Installing, deploying an mantaining a `swift openstack data storage service <https://docs.openstack.org/swift/latest/getting_started.html>`_ 
     is a nontrivial task. Therefore it is recommended to request access to this service to a provider.
     Be aware that **IT COSTS MONEY** to maintain the service running in a server!
   * The large files and their corresponding metadata are going to be stored in the `swift collection <https://docs.openstack.org/swift/latest/api/object_api_v1_overview.html>`_.
     using the same ``collection_name`` that has been specified in the :ref:`job metadata`.
