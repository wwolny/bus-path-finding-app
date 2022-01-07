#!/bin/bash

docker exec -it ejabberd bin/ejabberdctl register client localhost client_password
docker exec -it ejabberd bin/ejabberdctl register driver localhost driver_password
docker exec -it ejabberd bin/ejabberdctl register mathematician localhost mathematician_password
docker exec -it ejabberd bin/ejabberdctl register manager localhost manager_password
docker exec -it ejabberd bin/ejabberdctl register dummy localhost dummy_password
