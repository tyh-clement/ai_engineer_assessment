import csv
import time
from elasticsearch import Elasticsearch, helpers

ES_URL = "http://elasticsearch:9200"
INDEX = "cv-transcriptions"
CSV_PATH = "/data/cv-valid-dev.csv"

# 1. Wait until Elasticsearch is ready
es = Elasticsearch(ES_URL)
while not es.ping():
    print("Waiting for Elasticsearch...")
    time.sleep(3)

# 2. Start fresh each run so records aren't duplicated
if es.indices.exists(index=INDEX):
    es.indices.delete(index=INDEX)

# 3. Create the index and declare the field types
es.indices.create(index=INDEX, mappings={
    "properties": {
        "generated_text": {"type": "text"},
        "duration": {"type": "float"},
        "age": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "gender": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "accent": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
    }
})

# 4. One document per CSV row, skipping blank cells
def docs():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            doc = {k: v for k, v in row.items() if k and v and v.lower() != "nan"}
            yield {"_index": INDEX, "_source": doc}

# 5. Load everything in batches
ok, errors = helpers.bulk(es, docs(), raise_on_error=False)
print(f"Indexed {ok} records, {len(errors)} errors")