Compute
=======
The ``compute`` command ask the *web service* for available jobs that needs to be run.
To run some jobs you need to type in the terminal:
::

   moka compute input_compute.yml

Where the *input_compute.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`jobs input` metadata.

The compute command takes the user's input, request some available job and :ref:`schedule` those jobs using the information
provided by the user.


.. _jobs input:

Input File
**********

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

   # Job scheduler. Of of none, slurm or pbs (default: none)
   scheduler:
      slurm

   # Maximum number of jobs to request (default: 10)
   max_jobs:
      5
      
.. _schedule:

Job Scheduling
**************
Most of the scientific simulation are usually perform in supercomputers that use a
`job scheduler <https://en.wikipedia.org/wiki/Job_scheduler>`_. *Moka* supports two of the most popular ones: `SLURM <https://www.openpbs.org/>`_ and `PBS <https://www.openpbs.org/>`_.

If you choose a *scheduler* different from ``none``, *Moka* will automatically contact
the job scheduler.

.. _Job state

Job State
*********
The user's requested jobs are initially marked as ``RESERVERED``, in the web service to
avoid conflicts with other users. Then, if the jobs are sucessfully scheduled they
are marked as `RUNNING`. If there is a problem during the scheduling or subsequent
running step the job would be marked as `FAILED`.
