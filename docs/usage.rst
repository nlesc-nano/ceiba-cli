Usage
#####
The **moka** command line interface offers four actions to interact
with the `insilico web service <https://github.com/nlesc-nano/insilico-server>`_.
You can check them by trying the following command in your terminal:
::

   user>  moka --help

You should see something similar to:
::
   
    usage: moka [-h] {compute,report,query,add} ...

    positional arguments:
      {compute,report,query,add}
                            Interact with the properties web service
        compute             compute available jobs
        report              Report the results back to the server
        query               query some properties from the database
        add                 Add new jobs to the database

    optional arguments:
      -h, --help            show this help message and exit
