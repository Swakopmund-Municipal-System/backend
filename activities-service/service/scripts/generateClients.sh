#!/bin/bash

SPEC_URL="http://196.216.167.82/api/activities/openapi.json"

java -jar openapi-generator-cli.jar generate -i $SPEC_URL -g swift5 -o swift-client
java -jar openapi-generator-cli.jar generate -i $SPEC_URL -g kotlin -o kotlin-client
java -jar openapi-generator-cli.jar generate -i $SPEC_URL -g typescript-axios -o ts-client

echo "All clients generated."