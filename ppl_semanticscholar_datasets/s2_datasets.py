import json
from pathlib import Path
import shutil
from urllib.request import urlopen


# api tutorial: https://www.semanticscholar.org/product/api/tutorial
# examples: https://github.com/allenai/s2-folks/tree/main/examples/python
# bulk datasets api: https://api.semanticscholar.org/api-docs/datasets


class S2Datasets:
    '''
    Datasets API for SemanticScholar (S2).
    '''

    def __init__(self, s2_api, debug=False, iter_wrapper=None):
        '''
        :param str s2_api: an instance of S2API
        :param bool debug: if True, will print short messages about what the API is doing
        :param iter_wrapper: useful to keep track where in the stream the processing is. Ex - pass in tqdm instance. Ignored if None. 
        '''
        self._s2 = s2_api
        self._debug = debug
        self._iter_wrapper = iter_wrapper

    def download_all(self, dataset, dir_path):
        dir_path = Path(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)

        release_id = self._s2.release_id()
        self._dbg(f'Latest S2 release-id: {release_id}')
        shard_urls = self.shards(dataset, release_id)
        self._dbg(f'Found {len(shard_urls)} shards for dataset {dataset}')
        for k, shard_url in enumerate(shard_urls):
            self._dbg(f'Downloading shard #{k} or {len(shard_urls)}')
            self.download_shard(shard_url, dir_path / f'{dataset}_{k:03d}.gz')

    def download_shard(self, shard_url, file_path):
        with urlopen(shard_url) as response:
            with open(file_path, "wb") as f_out:
                shutil.copyfileobj(response, f_out)

    def stream_all(self, dataset, handler):
        '''
        :param str dataset: the name of the dataset. Ex - "papers".
        :param handler: function that receives each json record one by one. 
        '''
        release_id = self._s2.release_id()
        self._dbg(f'Latest S2 release-id: {release_id}')
        shard_urls = self.shards(dataset, release_id)
        self._dbg(f'Found {len(shard_urls)} shards for dataset {dataset}')
        for k, shard_url in enumerate(shard_urls):
            self._dbg(f'Processing shard #{k} or {len(shard_urls)}')
            self.stream_shard(shard_url, handler)

    def shards(self, dataset, release_id):
        '''
        :param str dataset: the name of the dataset. Ex - "papers".
        :param str release_id: the intended release-id.
        :returns: the URLs to each shard of dataset.
        :rtype: list
        '''
        return self._s2.release_files(dataset, release_id)

    def stream_shard(self, shard_url, handler):
        '''
        :param str shard_url: url to json content.
        :param handler: function that receives each json record one by one. 
        '''
        with self._s2.stream_gzip(shard_url) as f_in:
            self._stream_records(f_in, handler)

    def _stream_records(self, f_in, handler):
        it = self._stream_iter(f_in)
        for line in it:
            record = json.loads(line)
            handler(record)

    def _stream_iter(self, f_in):
        return self._iter_wrapper(f_in) if self._iter_wrapper else f_in

    def _dbg(self, msg):
        if self._debug:
            print(msg)

