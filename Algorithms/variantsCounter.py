import urllib
from collections import Counter
import operator
import urllib.request
import json

baseUrl = "http://cdbes-stage.hli.io:9200"
url = "/annotation/genome/_search"
body = """{
    "_source": false,
    "from": 0,  "size": 69271, 
    "query": {
        "bool": {}
    },
    "filter": {
        "and": {
            "filters": [
                {
                    "term": {
                        "filter": "PASS"
                    }
                },
                {
                    "range": {
                        "hli_af": {
                            "lte": 1
                        }
                    }
                },
                {
                    "terms": {
                        "gene_information.gene_symbol": [
                            "BRCA1"
                        ]
                    }
                }
            ]
        }
    },
    "fields": [
        "chrposrefalt"
    ]
}"""

#data = urllib.parse.urlencode(body)
req = urllib.request.Request(baseUrl + url, body.encode('ascii'))
res = urllib.request.urlopen(req)
the_page = res.read().decode('utf-8')
obj = json.loads(the_page)

variants = []

for x in obj["hits"]["hits"]:
    variants.append(x["fields"]["chrposrefalt"][0])

d_desc = sorted(Counter(variants).items(), key=operator.itemgetter(1), reverse=True)

print("Unique variants = " + str(len(d_desc)))
print("Total number of duplicates = " + str(obj["hits"]["total"]))
print("Avg duplicates per variant = " + str(sum(d[1] for d in d_desc) / len(d_desc)))

for i in d_desc:
    print ("{0} -- {1}".format(i[0], i[1]))