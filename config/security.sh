#! /bin/sh


/usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh \
    -cd /usr/share/opensearch/config/opensearch-security/ \
    -cacert /usr/share/opensearch/config/root-ca.pem \
    -cert /usr/share/opensearch/config/admin.pem \
    -key /usr/share/opensearch/config/admin-key.pem \
    -h $1 \
    -cn docker-cluster \
    -p 9200
