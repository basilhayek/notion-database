from notion_database.request import Request

class Search:
    def __init__(self, integrations_token):
        self.url = 'https://api.notion.com/v1/search'
        self.integrations_token = integrations_token
        self.result = {}
        self.request = Request(self.url, integrations_token=integrations_token)

    def search(self, query, sort, filter, start_cursor, page_size):
        body = {}
        if not filter is None:
            body['filter'] = filter
        self.result = self.request.call_api_post(self.url, body=body)

    def search_dbs(self):
        filter = {'value': 'database', 'property': 'object'}
        self.search(None, None, filter, None, None)

