import json
import os
from subprocess import Popen, PIPE        

# output = subprocess.Popen("docker exec -it dockervarnishnginx_varnish_1  varnishstat -j", shell=True,stdout=PIPE,stderr=PIPE)
p = Popen("cat /Users/emiltorlen/Documents/GIT/dynatrace-varnish-container/out.json", shell=True,stdout=PIPE,stderr=PIPE)
#print(output)
stdout, stderr = p.communicate()

print(stderr)
# print(stdout)
h=json.loads(stdout)
print(h["MAIN.cache_hit"]["value"])

# cmd = "docker exec -it dockervarnishnginx_varnish_1  varnishstat -j > /home/dtuser/out1.json"
# os.system(cmd)
# with open('/home/dtuser/out1.json') as f:
#     hits = json.load(f)
#     print(hits["MAIN.cache_hit"]["value"])

