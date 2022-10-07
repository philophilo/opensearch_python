# Python OpenSearch

## Local run

- create certificates
  `docker-compose -f docker-compose-certs.yml`

- Run opensearch
  `docker-compose up`

Note: client won't will fail since openseach will take a while to be ready
In a different terminal run the opensearch terminal
`docker-compose start opensearch-client`
