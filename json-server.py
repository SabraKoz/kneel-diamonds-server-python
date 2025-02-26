import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import get_all_orders, retrieve_order

class JSONServer(HandleRequests):

    def do_GET(self):
        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "orders":
            if url["pk"] != 0:
                response_body = retrieve_order(url["pk"], url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            response_body = get_all_orders(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        



def main():
    host = ''
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()