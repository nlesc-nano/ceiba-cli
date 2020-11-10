Query
=====
The ``query`` actions requests some data from the web service
and writes the requested data in a csv file.

There are currently two possible query actions:
 * request all the available data
 * request a single entry

To request some data, you need to type in the terminal:
::

   moka query -i input_query.yml

Where the *input_query.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing
the :ref:`query input` metadata.


.. _query input:

Querying all the Available Entries
----------------------------------
The following section describe the input to request all the available
data for a given collection.

Query Input File
****************

The input file contains the following mandatory keywords:
::

   # URL to the insilico server
   url:
      http://localhost:8080/graphql

   # Name of the collection to query
   collection_name:
      "candidates"

      
Other optional keywords are:
::

   # Path to the ouput file containing the properties in CSV format
   # (default="output_properties.csv")
   output_file:
      "path/to/output.csv"


Querying a Single Entry
-----------------------
In order to request a single entry from a whole collection,
you will need the same input that in the previous section plus the following
mandatory keyword:

::
   # Simplified molecular-input line-entry system (SMILE)
   smile: CC(=O)O
