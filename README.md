# TravelRouteRecommendation

Major Contributor : https://github.com/dodo9396

The details of the project is published here : https://www.semanticscholar.org/paper/A-spatial-clustering-approach-for-efficient-using-Deeksha-Ashrith/a3b210aaafc4dc011e2125248f8db4cca6e268a6?tab=abstract

A web application that suggests an optimal route between A and B such that multiple tourist attractions are present on the journey from A to B, finding a middle ground between shortest route and a route which includes maximum tourist attractions.

Install :

1) gensim - requires numpy and scipy
2) Rtree - requires libspatial index
3) imposm.parser
4) overpy
5) overpass
6) networkx
7) scikit
8) nltk
9) postgresql

        sudo apt-get install postgresql-9.3
    
10) pgrouting

        sudo add-apt-repository ppa:georepublic/pgrouting
        sudo apt-get update
        sudo apt-get install postgresql-9.3-pgrouting

11) postgis

        sudo apt-get install postgresql-9.3-postgis-2.1 postgresql-contrib pgadmin3
        sudo su -m postgres
        psql
        CREATE USER deeksha SUPERUSER;
        \q
        su deeksha
        createdb flickr
        psql -d flickr
        CREATE EXTENSION postgis;
        CREATE EXTENSION postgis_topology;
        CREATE EXTENSION fuzzystrmatch;
        CREATE EXTENSION postgis_tiger_geocoder;
        CREATE EXTENSION pgrouting;

12) osm2pgrouting

        sudo apt-get install cmake
        sudo apt-get install libpq-dev
        cmake -H. -Bbuild
        cd build/
        make
        make install


System overview : 

<img src="./images/System-Architecture.png" width="50%"/>

<img src="./images/Algorithm.png" width="50%"/>

<img src="./images/Output.png" width="50%"/>
