from gzip import GzipFile
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


# api tutorial: https://www.semanticscholar.org/product/api/tutorial
# examples: https://github.com/allenai/s2-folks/tree/main/examples/python
# bulk datasets api: https://api.semanticscholar.org/api-docs/datasets

BASE_URL = "https://api.semanticscholar.org/datasets/v1/release"


class S2API:
    '''
    Low-Level SemanticScholar (S2) API.
    '''

    def __init__(self, s2_api_key):
        '''
        :param str s2_api_key: the API key given to you by SemanticScholar
        '''
        self.s2_api_key = s2_api_key
        self.http = Session()
        self.http.mount('https://', HTTPAdapter(max_retries=Retry(
            # see https://github.com/urllib3/urllib3/blob/main/src/urllib3/util/retry.py#L39
            total=15,
            backoff_factor=2.0,
            respect_retry_after_header=True,
            status_forcelist=[502, 503, 504],
            allowed_methods=set({'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT', 'TRACE', 'POST'}),
        )))

    def _json(self, url):
        rsp = self.http.get(url, headers={'x-api-key': self.s2_api_key}, params={'limit': 10})
        rsp.raise_for_status()
        return rsp.json()

    def release_id(self):
        '''
        :returns: the latest S2 release-id.
        :rtype: str
        '''
        return self._json(BASE_URL)[-1]

    def release_files(self, dataset, release_id):
        '''
        :returns: the URLs to each shard of dataset.
        :rtype: list
        '''
        url = f'{BASE_URL}/{release_id}/dataset/{dataset}'
        return self._json(url)['files']

    def stream_gzip(self, url):
        '''
        :returns: a plain-text stream for the given url.
        :rtype: GzipFile
        '''
        resp = self.http.get(url, headers={'x-api-key': self.s2_api_key}, stream=True).raw
        return GzipFile(fileobj=resp)

