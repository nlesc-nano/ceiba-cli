Add (for Administrators)
########################
The ``add`` command is an adminstrative action to add new jobs into the database

To run some jobs you need to type in the terminal:
::

   moka add -i input_add.yml

Where the *input_compute.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`jobs input` specification.

.. _jobs input:

Add Input File
**************
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
      compute:
         workflow_name
      prop1:
         input_prop1
      prop2:
         input_prop2


How does it work?
*****************
Initially the ``add` command will extract from the ``target_collection`` the *smiles*
and their unique identifiers. Use those values it would generate a collection
with the new jobs to compute and a collection where the new properties are going
to be stored.
