#!/bin/bash

# This script runs only one instance of cassandra. And bind its /var/lib/cassandra directory to specified location
# (~/workspace/MEF/SPA/Server/Cassandra/1 for this example)

docker run --name spa_cassandra -v ~/workspace/MEF/SPA/Server/Cassandra/1:/var/lib/cassandra -d cassandra:latest