from django.http import HttpResponse, HttpResponseNotFound

from git.repo import Repo
from git.service import GIT_SERVICE_UPLOAD_PACK, GIT_SERVICE_RECEIVE_PACK

GIT_HTTP_INFO_REFS = 1
GIT_HTTP_SERVICE_UPLOAD_PACK = 2
GIT_HTTP_SERVICE_RECEIVE_PACK = 3


def get_http_error(exception):
    """
        Returns proper http failure status code according to the provided exception.
    """

    if 'Not a git repository' in exception.args[0]:
        return HttpResponseNotFound()


class GitResponse(HttpResponse):
    """
        Git http response.
    """

    def __init__(self, *args, **kwargs):
        self.service = kwargs.pop('service', None)
        self.action = kwargs.pop('action', None)
        self.repository = kwargs.pop('repository', None)
        self.data = kwargs.pop('data', None)
        super(GitResponse, self).__init__(*args, **kwargs)


    def get_packet_length(self, packet):
        """
            Returns length of the given packet in a 4 byte hex string.
            This string is placed at the beginning of the response body.

            e.g.
                001e
        """

        hex = '0123456789abcdef'
        length = len(packet) + 4
        prefix = hex[int((length >> 12) & 0xf)]
        prefix = prefix + hex[int((length >> 8) & 0xf)]
        prefix = prefix + hex[int((length >> 4) & 0xf)]
        prefix = prefix + hex[int((length) & 0xf)]

        return prefix


    def get_header_expires(self):
        """
            Returns 'Expires' header value.

            e.g.
                'Fri, 01 Jan 1980 00:00:00 GMT'
        """

        return 'Fri, 01 Jan 1980 00:00:00 GMT'


    def get_header_pragma(self):
        """
            Returns 'Pragma' header value.

            e.g.
                'no-cache'
        """

        return 'no-cache'


    def get_header_cache_control(self):
        """
            Returns 'Cache-Control' header value.

            e.g.
                'no-cache, max-age=0, must-revalidate'
        """

        return 'no-cache, max-age=0, must-revalidate'


    def get_header_content_type(self):
        """
            Creates the 'Content-Type' header according to the requested service and action.
            Structure of a 'Content-Type' header is 'application/x-\{service\}-\{action\}'

            e.g.
                'application-git-receive-pack-advertisement'
        """

        return 'application/x-{0}-{1}'.format(self.service, self.action)


    def set_response_header(self):
        """
            Sets response headers, according to the requested service and action.
            Header contains values such as 'Expires', 'Pragma', 'Cache-Control' and 'Content-Type'.
        """

        self.__setitem__('Expires', self.get_header_expires())
        self.__setitem__('Pragma', self.get_header_pragma())
        self.__setitem__('Cache-Control', self.get_header_cache_control())
        self.__setitem__('Content-Type', self.get_header_content_type())


    def set_response_first_line(self):
        """
            Sets first line of git response that includes length and requested service.

            e.g.
                001f# service=git-receive-pack
        """

        first_line = '# service={0}\n'.format(self.service)
        prefix = self.get_packet_length(first_line)
        self.write('{0}{1}0000'.format(prefix, first_line))


    def set_response_payload(self, payload_type):
        """
            Writes 'refs' object information of the given repository to http response.
        """

        if payload_type == GIT_HTTP_INFO_REFS:
            self.write(self.repository.get_info_refs(self.service))
        elif payload_type == GIT_HTTP_SERVICE_RECEIVE_PACK:
            self.write(self.repository.commit(self.data))
        elif payload_type == GIT_HTTP_SERVICE_UPLOAD_PACK:
            self.write(self.repository.pull(self.data))


    def get_http_info_refs(self):
        """
            Returns a HttpResponse for info/refs requests.
        """

        try:
            self.set_response_header()
            self.set_response_first_line()
            self.set_response_payload(GIT_HTTP_INFO_REFS)
            return self
        except BaseException as e:
            return get_http_error(e)


    def get_http_service_rpc(self):
        """
            Returns a HttpResponse to 'git-upload-pack', 'git-receive-pack' requests.
        """

        try:
            self.set_response_header()
            if self.service == GIT_SERVICE_RECEIVE_PACK:
                self.set_response_payload(GIT_HTTP_SERVICE_RECEIVE_PACK)
            elif self.service == GIT_SERVICE_UPLOAD_PACK:
                self.set_response_payload(GIT_HTTP_SERVICE_UPLOAD_PACK)
            return self
        except BaseException as e:
            return get_http_error(e)
