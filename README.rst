graph-vl
========

.. image:: https://github.com/verifid/graph-vl/workflows/graph-vl%20ci/badge.svg
    :target: https://github.com/verifid/graph-vl/actions

.. image:: https://codecov.io/gh/verifid/graph-vl/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/verifid/graph-vl

Self deployed identity verification layer with GraphQL.

Introduction
------------

graph-vl is the verification layer of verifid developed with GraphQL. It's the secondary core project other than `VL <https://github.com/verifid/vl/>`_ 
that is responsible from verifying identity cards or passports. Basically it's a self deployed API which has 3 main endpoints. It runs on either Docker or
Kubernetes as a container. All endpoints have detailly documented using GraphiQL and project relies on some other VerifID and as well as other Open Source
Python modules.

For storage, it uses Postgres as a database and SQLAlchemy as an object relational mapper. To make it simple DB has only two tables which is enough for this
project.

Requirements
------------

* Python 3.6+
* Run time dependencies ``requirements.txt``
* Test dependencies ``requirements.testing.txt``

Usage
-----

To run the **graph-vl** server, please execute the following command from the root directory

.. code::

    pip3 install -r requirements.txt
    source ./set_environment_variables.sh env-postgres.env
    uvicorn graphvl.main:app

All endpoints available on

``http://127.0.0.1:8000``
