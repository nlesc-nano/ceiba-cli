.. image:: https://github.com/nlesc-nano/moka/workflows/build/badge.svg
   :target: https://github.com/nlesc-nano/moka/actions
.. image:: https://readthedocs.org/projects/moka-command-line-interface/badge/?version=latest
   :target: https://moka-command-line-interface.readthedocs.io/en/latest/?badge=latest
.. image:: https://codecov.io/gh/nlesc-nano/Moka/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/nlesc-nano/Moka
.. image:: https://zenodo.org/badge/296641388.svg
   :target: https://zenodo.org/badge/latestdoi/296641388

####
moka
####

command line interface to interact to interact with the `insilico web server <https://github.com/nlesc-nano/insilico-server>`_.
See the `documentation <https://moka-command-line-interface.readthedocs.io/en/latest/>`_.


Installation
------------

To install moka, do:

.. code-block:: console

  pip install git+https://github.com/nlesc-nano/moka.git@master	

Authentication
##############

Generate an OAuth token
-----------------------
You need to generate an **OAuth token from GitHub** in order to login into the application!
For doing so, you should:

1. Go to `github tokens <https://github.com/settings/tokens>`_ and click the ``Generate new token`` button.
2. Provide your GitHub password when prompted
3. Fill in a description for the token, for example, *insilico access token*.
4. **Do not enable any scope** therefore the token will grant read-only access to the app
5. Click ``Generate`` at the bottom. Make sure to copy its value because we'll need it to login!


Contributing
############

If you want to contribute to the development of moka,
have a look at the `contribution guidelines <CONTRIBUTING.rst>`_.

License
#######

Copyright (c) 2020, Netherlands eScience Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



Credits
#######

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `NLeSC/python-template <https://github.com/NLeSC/python-template>`_.
