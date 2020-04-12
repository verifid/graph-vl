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
Kubernetes as a container. All endpoints are documented using GraphiQL and project relies on VerifID and other Open Source 
Python modules.

For storage, it uses Postgres as a database and SQLAlchemy as an object relational mapper. To make it simple DB has only two tables which is enough for this project.

There is only four steps to veriy an identity of a person which you can find those steps below.

1. Create a user with personal details
2. Upload user's selfie photo
3. Take a photo of front page of identity card or passport, then upload
4. Call verify endpoint and get the result

Requirements
------------

* Python 3.6+
* Postgres
* Run time dependencies ``requirements.txt``
* Test dependencies ``requirements.testing.txt``

Usage
-----

You need a Postgres instance in your machine our a Docker container that runs database. To pull docker image
and start a container

.. code::

    docker pull postgres:11.5
    docker run --name postgres -e POSTGRES_SERVER=localhost \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_DB=postgres \
        -d -p 5432:5432 postgres:11.5
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres
    # We will use this IP address when we build or run graph-vl

To run the **graph-vl** server, please execute the following commands from the root directory

.. code::

    docker build --build-arg PG_SERVER=${POSTGRES_IP_ADDRESS} \
        --build-arg PG_USER=postgres \
        --build-arg PG_PASSWORD=postgres \
        --build-arg PG_DB=postgres \
        -t graphvl .
    docker run --rm -it -d -p 8000:8000 --name graph-vl graphvl:latest

    docker build -t graphvl .
    docker run -e PG_SERVER=${POSTGRES_IP_ADDRESS} \
        -e PG_USER=postgres \
        -e PG_PASSWORD=postgres \
        -e PG_DB=postgres \
        --rm -it -d -p 8000:8000 \
        --name graph-vl graphvl:latest env

Interface
---------

+-----------------+---------------+-----------------+
||image_expolorer|||image_queries|||image_mutations||
+-----------------+---------------+-----------------+ 

All endpoints available on

``http://127.0.0.1:8000``

.. |image_expolorer| image:: https://raw.githubusercontent.com/verifid/graph-vl/master/resources/explorer.png
.. |image_queries| image:: https://raw.githubusercontent.com/verifid/graph-vl/master/resources/queries.png
.. |image_mutations| image:: https://raw.githubusercontent.com/verifid/graph-vl/master/resources/mutations.png
