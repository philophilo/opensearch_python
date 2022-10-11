import json
import boto3
import time
import os
from opensearchpy import (
			OpenSearch,
			RequestsHttpConnection,
			AWSV4SignerAuth,
			exceptions,
		)

from create_alias import Alias
from create_index import Index

TEMPLATE_NAME = "opster-template100"
INDEX = "opster-1"

# alias, index == only

ALIAS = ["movies"]
INDEX = ["great-movies-add-*"]
INDEX_NAME = "great-movies-add-1"
INDEX_DELETE = True
ALIAS_UPDATE = True
ALIAS_DELETE = True
ALIAS_BODY = {
	"actions":[
		{
			"add": {
				"alias": "movies2",
				"index": "great-movies-*"
			}
		}
	]
}
DELETE_ALIAS = [True, "movies"]


# create local client
def create_client():
	host = 'opensearch-node1'
	port = 9200
	auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
	ca_certs_path = '/certs/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.
	index_name = "python-test-index"

	# Create the client with SSL/TLS enabled, but hostname verification disabled.
	try:
		client = OpenSearch(
			hosts=[{'host': host, 'port': port}],
			http_compress=True, # enables gzip compression for request bodies
			http_auth=auth,
			client_cert='/certs/client-cert.pem',
			client_key='/certs/client-key.pem',
			use_ssl=True,
			verify_certs=True,
			ssl_assert_hostname=False,
			ssl_show_warn=False,
			ca_certs=ca_certs_path
		)
		print("Connected to opensearch host: {}".format(host))
		return client
	except exceptions.ConnectionError as e:
		print("Error: {} Failed to connect to opensearch".format(e))

client = create_client()
print("===>>>", client)

def index():
	with open("./movies_index.json", "r") as read_file:
 		data = json.load(read_file)
	index = Index(client, INDEX_NAME)
	index_exists = index.check()

	print(index_exists, "<<<<")
	try:
		response = index.create()
		print(response, "*******", index_exists)
	except exceptions.RequestError as e:
		response = index.get()
		print("{}: index exists {}".format(e, response))

	if INDEX_DELETE:
		response = index.delete()
		print(response, "*******", index.check())
	

def alias_setup():
	alias = Alias(client, ALIAS, INDEX)
	alias_exists = alias.check_alias()

	response = alias.update_alias(body=ALIAS_BODY)
	print(response, "****", alias.get_alias())

	response = alias.create_alias()
	print("....", response['acknowledged'])
	
	if ALIAS_UPDATE:
		response = alias.update_alias(body=ALIAS_BODY)
		print(response, "----", alias.get_alias())
		

alias_setup()
index()

# # start ECS function
# def ecs():
# 	host = os.environ.get('HOST')
# 	region = os.environ.get('REGION')
# 	credentials = boto3.Session().get_credentials()
# 	auth = AWSV4SignerAuth(credentials, region)
# 	client = OpenSearch(
# 		hosts=[{'host': host, 'port': 443}],
# 		http_auth=auth,
# 		use_ssl=True,
# 		verify_certs=True,
# 		connection_class=RequestsHttpConnection
# 	)
# 	index_name = "python-test-index"
# 	log_types = ['hadoop', 'hdfs', 'spark', 'zoo_keeper']
# 	for log_type in log_types:
# 		counter = 0
# 		with open('./sample_logs/' + log_type + '.txt', encoding='utf-8') as log_file:
# 			for row in log_file:
# 				data = '{"log_message":"' + row.strip() + '"}'
# 				response = client.index(
# 					index = index_name,
# 					body = {
# 						'data': data
# 					},
# 					id = counter,
# 					refresh = True
# 				)
# 				# time.sleep(1)
# 				print(log_type + " log # " + str(counter) + " / " + '2000' + " sent")
# 				counter = counter + 1
# # end ECS function


# # create local client
# def create_client():
# 	host = 'opensearch-node1'
# 	port = 9200
# 	auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
# 	ca_certs_path = '/certs/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.
# 	index_name = "python-test-index"

# 	# Create the client with SSL/TLS enabled, but hostname verification disabled.
# 	try:
# 		client = OpenSearch(
# 			hosts=[{'host': host, 'port': port}],
# 			http_compress=True, # enables gzip compression for request bodies
# 			http_auth=auth,
# 			client_cert='/certs/client-cert.pem',
# 			client_key='/certs/client-key.pem',
# 			use_ssl=True,
# 			verify_certs=True,
# 			ssl_assert_hostname=False,
# 			ssl_show_warn=False,
# 			ca_certs=ca_certs_path
# 		)
# 		print("Connected to opensearch host: {}".format(host))
# 		return client
# 	except exceptions.ConnectionError as e:
# 		print("Error: {} Failed to connect to opensearch".format(e))

# # start sample json file template
# def get_template(client):
# 	k = client.indices.exists_index_template(name=TEMPLATE_NAME)
# 	if k:
# 		response = client.indices.get_index_template(name=TEMPLATE_NAME)
# 		print(">>>>", response)
# 		print("{} Index template not found".format(TEMPLATE_NAME))
# 		return True
# 	return False


# def template(client):
# 	if get_template(client):
# 		print("{} Index Template already exists".format(TEMPLATE_NAME))
# 	else:
# 		with open("/app/index_template.json", "r") as read_file:
# 			data = json.load(read_file)

# 		try:
# 			client.indices.put_index_template(
# 				name=TEMPLATE_NAME,
# 				body=data
# 			)
# 			print("{} Index template created".format(TEMPLATE_NAME))
# 		except exceptions.RequestError as e:
# 			print(e, "{} Index Template already exists".format(TEMPLATE_NAME))
# # end sample json file template


# # start indexing movies
# def create_movies_index_template(client):
# 	with open("/app/movies_index_template.json", "r") as read_file:
# 		data = json.load(read_file)
# 	try:
# 		client.indices.put_index_template(
# 			name="great-movies-add-template",
# 			body=data
# 		)
# 		print("{} Index template created".format("movies-template"))
# 	except exceptions.RequestError as e:
# 		print(e, "{} Index Template already exists".format("movies-template"))


# def index_movies(client):
# 	with open("./data/movies.json", "r") as read_file:
# 		data = json.load(read_file)
	
# 	for k, v in enumerate(data['movies']):
# 		response = client.index(
# 			index="great-movies-add-3",
# 			body=v,
# 			refresh = True
# 		),
# 		id=k
# 		print(">>>>>>", response, k, v)
# # end indexing movies
	
# # start quick sample
# def create_index(client):
# 	response = client.index(
# 		index=INDEX,
# 		body={
# 		"id": 158,
# 		"location": "1.486912, 2.493157",
# 		"movie": "Harry Potter"
# 		},
# 		refresh=True
# 	)
# 	print(response)


# def get_index(client):
# 	response = client.indices.get(
# 			index=[INDEX]
# 		)
# 	print(response)

# # end quick sample


# # Start local logs
# def dev():
# 	host = 'opensearch-node1'
# 	port = 9200
# 	auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
# 	ca_certs_path = '/certs/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.
# 	index_name = "python-test-index"

# 	# Create the client with SSL/TLS enabled, but hostname verification disabled.
# 	client = OpenSearch(
# 		hosts = [{'host': host, 'port': port}],
# 		http_compress = True, # enables gzip compression for request bodies
# 		http_auth = auth,
# 		client_cert = '/certs/client-cert.pem',
# 		client_key = '/certs/client-key.pem',
# 		use_ssl = True,
# 		verify_certs = True,
# 		ssl_assert_hostname = False,
# 		ssl_show_warn = False,
# 		ca_certs = ca_certs_path
# 	)

# 	log_types = ['hadoop', 'hdfs', 'spark', 'zoo_keeper']
# 	for log_type in log_types:
# 		counter = 0
# 		with open('./sample_logs/' + log_type + '.txt', encoding='utf-8') as log_file:
# 			for row in log_file:
# 				data = '{"log_message":"' + row.strip() + '"}'
# 				response = client.index(
# 					index=index_name,
# 					body={
# 						'data': data
# 					},
# 					id=counter,
# 					refresh = True
# 				)
# 				# time.sleep(1)
# 				print(log_type + " log # " + str(counter) + " / " + '2000' + " sent")
# 				counter = counter + 1
# # End local logs


# # TODO add function to poll opensearch until it is ready

# if os.environ.get('ENV') == "dev":
# 	# run ecs example
# 	ecs()
# else:
# 	client = create_client()
# 	template(client)
# 	# run quick sample
# 	create_index(client)
# 	get_index(client)
# 	# run movies
# 	create_movies_index_template(client)
# 	index_movies(client)
# 	# run local logs
# 	dev()