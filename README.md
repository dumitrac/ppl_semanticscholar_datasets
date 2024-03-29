# Unofficial SDK for SemanticScholar Datasets API

Use this for processing large datasets of hundreds of millions of records.
If you want to processes millions of records, in order to scale better than querying the Academic Graph API millions of times, you'd instead use the Datasets API to stream 30 or 60 gzip shards of all those records.

This package gets you ready for using the S2 Dataset API.


## Setup:
This section is only about instantiating the SDK:

### Ex-1: no debug feature
```
from s2_api import S2API
from s2_datasets import S2Datasets

s2 = S2API(s2_api_key)
datasets = S2Datasets(s2)
```

### Ex-2: you want the SDK to print messages about what it iss doing
```
from s2_api import S2API
from s2_datasets import S2Datasets

s2 = S2API(s2_api_key)
datasets = S2Datasets(s2, debug=True, iter_wrapper=tqdm)
```

## Usage - streaming:
Now that the SDK is instantiated, let's use it to process the stream of json records.

### Ex-1: you want to process all the shards in the dataset
```
from pprint import pprint

datasets.stream_all("papers", lambda r: pprint(r))
```

### Ex-2: you want to process only specific shards of the dataset
```
from pprint import pprint

release_id = s2.release_id()
shard_urls = datasets.shards("papers", release_id)
for shard_url in shard_urls:
    datasets.stream_shard(shard_url, lambda r: pprint(r))
```

## Usage - downloading:
Now that the SDK is instantiated, let's use it to download the dataset to disk.

### Ex-1: you want to download all the shards in the dataset
```
datasets.download_all("papers", "/tmp")
```

### Ex-2: you want to download only specific shards of the dataset
```
release_id = s2.release_id()
shard_urls = datasets.shards("papers", release_id)
datasets.download_shard(shard_urls[0], "D:/tmp/shard_0.gz")
```


## How to install
```
pip install git+https://github.com/dumitrac/ppl_semanticscholar_datasets.git
```


## Contact

Email to admin@papelist.app .

Also check out our app that enables you to explore and discover a research field of study independently - https://papelist.app .

See our Semantic Scholar gallery page at https://www.semanticscholar.org/api-gallery/papelist-app .

Follow us on X / Twitter at https://twitter.com/papelist_app .

