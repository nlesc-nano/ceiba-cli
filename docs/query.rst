Query
=====
The ``query`` actions requests some data from the web service
and writes the requested data in a csv file.

There are currently two possible query actions:
 * request what collections are available
 * request a single collection

To request what collections are available you just need to run the following command:
::

   ceibacli query -w http://yourCeibaInstance:8080/grapqhl

Previous command will ouput something similar to:
::

   Available collections:
  name size
  simulation1 3
  simulation2 42
  ....

In the previous ``name`` indicates the actual collections' names and ``size`` how many datasets are stored
in that particular collection.

To request all the datasets available in a given collection, you just need to run the following command:
::
   
   ceibacli query -w http://yourCeibaInstance:8080/grapqhl -c simulation2

That command will write into your current work directory a file called ``output_properties.csv``
containing the properties in the requested collection.
