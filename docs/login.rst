Login
#####
We certainly want to restrict who can access and modify the data. Therefore users are required
to login with the web service. For doing so, you should have a `GitHub account <https://github.com/>`_,
then you need to request a **read-only** token from `GitHub personal access token service <https://github.com/settings/tokens>`_.

Once you have a read-only GitHub token, you can login into the web service like:
::

  ceibacli login -w http://YourCeibaInstance.org:8080/graphql -t Your_token

How does it work?
#################
The *Ceiba server* will contact `GitHub <https://github.com/>`_ and will check if you are a known user there.
