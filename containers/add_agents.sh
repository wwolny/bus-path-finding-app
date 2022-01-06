#!/bin/bash

docker exec -it ejabberd bin/ejabberdctl register client localhost client_password
docker exec -it ejabberd bin/ejabberdctl register driver localhost driver_password
docker exec -it ejabberd bin/ejabberdctl register mathematitian localhost mathematitian_password
docker exec -it ejabberd bin/ejabberdctl register manager localhost manager_password
