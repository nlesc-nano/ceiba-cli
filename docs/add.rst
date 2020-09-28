Add (for Administrators)
########################
The ``add`` command is an adminstrative action to add new jobs into the database

To run some jobs you need to type in the terminal:
::

   moka add input_add.yml

Where the *input_compute.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`jobs input` specification.

.. _jobs input:

Input File
**********
The input file contains the following mandatory keywords:
::

   # URL to the insilico server
   url:
      http://localhost:8080/graphql

   # Target collection to get the smiles from
   target_collection:
     candidates

   # Name of the new collection to store the properties
   new_collection:  "PBE/DZP"

   # Settings to run the calculations in YAML format
   settings:
      prop1:

How does it work
****************
