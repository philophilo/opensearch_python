class Index:

    def __init__(self, client, name, body=None):
        self.index = name
        self.client = client
        self.body = body

    def create(self):
        return self.client.indices.create(
			index=self.index
		)

    def get(self):
        return self.client.indices.get(
            index=[self.index]
        )

    def check(self):
        return self.client.indices.exists(
			index=self.index
        )

    def delete(self):
        return self.client.indices.delete(
            index=self.index
        )