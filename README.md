# Python OpenSearch

## Local run

- create certificates
  `docker-compose -f docker-compose-certs.yml`

- Run opensearch
  `docker-compose up`

Note: client will fail since openseach will take a while to be ready.

In a different terminal run the opensearch client

`docker-compose start opensearch-client`
