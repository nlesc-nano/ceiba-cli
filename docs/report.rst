
Report
======
The ``report`` command send the results of the jobs computed by the user to
the web service. You can also send "standalone" data to the server. Where standalone
means data that is not associated to a job in the server, for example because it
has been previously computed.

To report the results you need to type in the terminal:
::

   moka compute input_report.yml

Where the *input_compute.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`report input` metadata.


If

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
   pattern: "results*csv"

   # The data to report is not associated to a job (default False)
   is_standalone: True


Jobs Metadata
*************
Apart from the computed data, the ``report`` command would try to collect some
metadata associated with the job like *username*, *platform*, etc. that
is fundamental for reproducibility purposes.
