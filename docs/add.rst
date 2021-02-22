Add (for Administrators)
########################
The ``add`` command is an adminstrative action to add new jobs into the database.

To add jobs you need to run the following command in the terminal:
::

   ceibacli add -w http://yourCeibaInstance:8080/grapqhl -c collection_name  -j Path/to/jobs.json

Where the `-w` option is the web service URL. the `collection_name` is the collection where the data is going to be stored.
Finally, the `-j` options is the path to the *JSON* file containing the jobs as an array of JSON objects.
See the next :ref:`jobs file` section for further information.

.. _jobs file:

Jobs File
*********
The job file is a list of json objects, like:
::

  [
      {
          "type": "awesome_simulation_1",
          "parameters": {
              "value": 3.14
          }
      },
      {
          "type": "awesome_simulation_2",
          "parameters": {
              "value": 2.187
          }
      }
  ]

Each job is a JSON object with the parameters to perform the simulation.
  
How does it work?
*****************
The `add` command will read each job in the JSON jobs file. For each job
it will generate a unique identifiers. Then, the jobs and their identifier will
be stored a collection named `job_your_collection_name`.
