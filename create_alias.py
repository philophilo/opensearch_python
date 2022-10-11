class Alias:

    def __init__(self, client, name, index):
        self.alias = name
        self.index = index
        self.client = client

    def create_alias(self):
        return self.client.indices.put_alias(
            name=self.alias,
			index=self.index
		)

    def get_alias(self):
        return self.client.indices.get_alias(
            name=self.alias
        )

    def check_alias(self):
        return self.client.indices.exists_alias(
            name=self.alias,
			index=self.index
        )

    def update_alias(self, body):
        return self.client.indices.update_aliases(
            body=body
        )

    def delete_alias(self):
        return self.client.indices.delete_aliases(
            body=body
        )