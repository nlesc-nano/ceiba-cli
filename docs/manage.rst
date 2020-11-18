Manage (For administrators)
###########################
The ``manage`` command is an adminstrative action to change the jobs status. For example,
jobs that have been marked as ``RESERVED`` or ``RUNNING`` for a long period of time
can be marked again as ``AVAILABLE`` if the user doesn't report the results.

To change the jobs status you need to type in the terminal:
::

   moka manage -i input_manage.yml

Where the *input_manage.yml* is an file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_ containing the :ref:`jobs metadata` specification.

.. _jobs metadata:

Manage Input File
*****************
The following snippet represent an input example for the *manage* action:
::

   # Target collection to change job status
   collection_name: "functional/basisset"

   # Metadata to change jobs status
   change_status:
    old_status: RUNNING
    new_status: AVAILABLE
    expiration_time: 24 # one day

How does it work?
*****************
Moka will research in the ``collection_name`` for all the jobs with ``old_status`` then
it will check if those jobs have been scheduled before the ``expiration_time``. If
the jobs have expired, Moka will marked the expired jobs with the ``new_status``.
 



