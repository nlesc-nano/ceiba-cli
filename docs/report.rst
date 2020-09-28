Report
======
The ``report`` command send the results of the jobs computed by the user to
the web service.
To report the results you need to type in the terminal:
::

   moka compute input_compute.yml

Where the *input_compute.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`report input` metadata.


.. _report input:

Input File
**********
The input file contains the following mandatory keywords:
::

   # URL to the insilico server
   url:
      http://localhost:8080/graphql

   # Name of the collection to update
   collection_name:
      "PBE/DZVP"

   # Path to the csv containing the results
   path_results: str



Jobs Metadata
*************
Apart from the computed data, the ``report`` command would try to collect some
metadata associated with the job like *username*, *platform*, etc. that
is fundamental for reproducibility purposes.
