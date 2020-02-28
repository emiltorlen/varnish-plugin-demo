import json

with open('out.json') as f:
    hits = json.load(f)
    print(hits["MAIN.cache_hit"]["value"])