#! /bin/bash

export $(echo $(cat .env | sed 's/#.*//g' | sed 's/\r//g' | xargs) | envsubst)

./app/manage.py ${@}
