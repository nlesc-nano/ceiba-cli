Usage
#####
The **ceibacli** command line interface offers four actions to interact
with the `insilico web service <https://github.com/nlesc-nano/insilico-server>`_.
You can check them by trying the following command in your terminal:
::

   user>  ceibacli --help

You should see something similar to:
::

    usage: ceibacli [-h] [--version] {compute,report,query,add,manage} ...

    positional arguments:
      {compute,report,query,add,manage}
                            Interact with the properties web service
        compute             compute available jobs
        report              Report the results back to the server
        query               query some properties from the database
        add                 Add new jobs to the database
        manage              Change jobs status

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit

After running one of the previous commands a log file named ``ceibacli_output.log``
is generated.
