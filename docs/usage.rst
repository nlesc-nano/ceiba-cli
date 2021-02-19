Usage
#####
The **ceibacli** command line interface offers four actions to interact
with the `insilico web service <https://github.com/nlesc-nano/insilico-server>`_.
You can check them by trying the following command in your terminal:
::

   user>  ceibacli --help

You should see something similar to:
::

  usage: ceibacli [-h] [--version] {login,add,compute,report,query,manage} ...

  positional arguments:
    {login,add,compute,report,query,manage}
                          Interact with the properties web service
      login               Log in to the Insilico web service
      add                 Add new jobs to the database
      compute             Compute available jobs
      report              Report the results back to the server
      query               Query some properties from the database
      manage              Change jobs status

  optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit


After running one of the previous commands a log file named ``ceibacli_output.log``
is generated.
