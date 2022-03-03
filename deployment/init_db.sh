#!/bin/sh


echo "Initializing postgres db..."

while ! nc -z 0.0.0.0 5432; do
  sleep 1
done

echo "postgres database has been successfully initialized"
fi

exec "$@"
