#!/bin/sh
echo "Waiting for user_service..."
until curl -s http://user_service:8000/graphql > /dev/null; do
  sleep 2
done

echo "Waiting for blog_service..."
until curl -s http://blog_service:8000/graphql > /dev/null; do
  sleep 2
done

echo "Starting gateway..."
exec "$@"
