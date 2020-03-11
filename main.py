import tistory as ts
import datetime
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(current_dir + '/api_keys.json', 'r') as fp:
    keys = json.load(fp)

tistory = ts.Tistory(api_keys=keys['tistory'])
# tistory.getList(1)
tistory.writePost("test", "content", 0, '')

