Compute
=======
The ``compute`` command ask the *web service* for available jobs that needs to be run.
To run some jobs you need to type in the terminal:
::

   moka compute

Or if you want to have more control over what is reported you can provide an input file like:
::

   moka compute -i input_compute.yml

Where the *input_compute.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`compute input` metadata.

The compute command takes the user's input, request some available job and :ref:`schedule` those jobs using the information
provided by the user.


.. _compute input:

Compute Input File
******************

The input file contains the following mandatory keywords:
::

   # URL to the insilico server
   url:
      http://localhost:8080/graphql

   # Name of the collection to compute
   collection_name:
      "PBE/DZVP"


Other optional keywords are:
::

   # Configuration of the job scheduler
   scheduler:
      "none"

   # Command use to run the workflow (default: compute_properties)
   command:
      compute_properties

   # Path to the directory where the calculations are going to run (default: workdir_moka)
   workdir:
      /path/to/workdir

   # Maximum number of jobs to request (default: 10)
   max_jobs:
      5
      
.. _schedule:

Job Scheduling
**************
Most of the scientific simulation are usually perform in supercomputers that use a
`job scheduler <https://en.wikipedia.org/wiki/Job_scheduler>`_. *Moka* supports two of the most popular ones: `SLURM <https://www.openpbs.org/>`_.
If you choose a *scheduler* different from ``none``, *Moka* will automatically contact
the job scheduler with the options that you have provided. Below you can find a description
of the available options:
::

   # Job scheduler. Of of "none" or "slurm" (default: none)
   scheduler:
      slurm
   
   # Number of computing nodes to request (default: 1)
   nodes:
      1

   # Number of CPUs per task (default: None)
   cpus_per_task:
      48

   # Total time to request ind "days:hours:minutes" format (default: 1day)
   walltime:
     "01:00:00"

   # Partion name (queue's name) where the job is going to run (default: None)
   partion_name:
     "short"

You can alternatively provide a string with all the options for the queue system like,
::

   scheduler:
     slurm
   
   # String with user's Configuration
   free_format: "#!/bin/bash
   #SBATCH -N 1
   #SBATCH -t 00:15:00
   ....
   "


.. _Job state:

Job State
*********
The user's requested jobs are initially marked as ``RESERVERED``, in the web service to
avoid conflicts with other users. Then, if the jobs are sucessfully scheduled they
are marked as `RUNNING`. If there is a problem during the scheduling or subsequent
running step the job would be marked as `FAILED`.
