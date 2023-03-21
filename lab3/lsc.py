# import requests
# import base64
# import json
# import time
# from tqdm import tqdm
#
# JOBS_ENDPOINT = 'https://submit.plgrid.pl/api/jobs'
# PLGDATA_ARES_DOWNLOAD_ENDPOINT = 'https://data.plgrid.pl/download/ares'


# class JobExecutor:
#     JOBS_ENDPOINT = 'https://submit.plgrid.pl/api/jobs'
#     PLGDATA_ARES_DOWNLOAD_ENDPOINT = 'https://data.plgrid.pl/download/ares'
#
#     def __init__(self, proxy_path):
#         self.proxy = self.get_proxy(proxy_path)
#
#     @staticmethod
#     def get_proxy(filepath):
#         with open(filepath, 'rb') as f:
#             proxy = f.read()
#
#         # imitate command proxy="`cat {path-to-proxy} | base64 | tr -d '\n'`"
#         encoded_proxy = str(base64.b64encode(proxy))[2:-1].replace('\n', '')
#         return encoded_proxy
#
#     def run_job(self, script):
#
#         headers = {
#             "Content-Type": "application/json",
#             "PROXY": f"{self.proxy}",
#         }
#
#         data = json.dumps({
#             "host": "ares.cyfronet.pl",
#             "script": script,
#         })
#
#         response = requests.post(self.JOBS_ENDPOINT, headers=headers, data=data)
#         response_data = response.json()
#         job_id = response_data['job_id']
#
#         return job_id
#
#     def monitor_job(self, job_id, rep_time=5):
#
#         headers = {
#             "PROXY": f"{self.proxy}"
#         }
#
#         url = '/'.join([self.JOBS_ENDPOINT, job_id])
#
#         time.sleep(5)
#
#         before = time.time()
#
#         while True:
#             response = requests.get(url, headers=headers)
#
#             response_data = response.json()
#             status = response_data['status']
#             current = time.time()
#             print(f'Time passed: {int(current - before)} s')
#             print(f'Job status: {status}')
#
#             if status == 'FINISHED':
#                 return
#
#             time.sleep(rep_time)
#
#     def download_file(self, remote_filepath, local_filepath):
#         headers = {
#             "PROXY": f"{self.proxy}"
#         }
#         url = ''.join([self.PLGDATA_ARES_DOWNLOAD_ENDPOINT, remote_filepath])
#         with requests.get(url, headers=headers, stream=True) as r:
#             r.raise_for_status()
#             with open(local_filepath, 'wb') as f:
#                 for chunk in tqdm(r.iter_content(chunk_size=8192)):
#                     f.write(chunk)
#
#
# if __name__ == '__main__':
#     job_exec = JobExecutor('x509up_u113905')
#     script = '#!/bin/bash\n sleep60'
#     job_id = job_exec.run_job(script)
#     print(f'Job {job_id} has been queued')
#     job_exec.monitor_job(job_id, 10)
#     print('Downloading results')
#     # remote_output = '/net/people/plgrid/plgdawid126/img_1png0001.png'
#     # job_exec.download_file(remote_output, './img_1png0001.png')

import requests
import base64
import json
import time
from tqdm import tqdm

JOBS_ENDPOINT = 'https://submit.plgrid.pl/api/jobs'
DOWNLOAD_ENDPOINT = 'https://data.plgrid.pl/download/ares'

with open('x509up_u113905', 'rb') as f:
    proxy = f.read()

proxy = str(base64.b64encode(proxy))[2:-1].replace('\n', '')
script = '#!/bin/bash\ncd /net/people/plgrid/plgdawid126/\nbash render.sh'
headers = {
    "Content-Type": "application/json",
    "PROXY": f"{proxy}",
}

data = json.dumps({
    "host": "ares.cyfronet.pl",
    "script": script,
})

response = requests.post(JOBS_ENDPOINT, headers=headers, data=data)
response_data = response.json()
job_id = response_data['job_id']
print("Job id ", job_id)

headers = {
    "PROXY": f"{proxy}"
}

url = '/'.join([JOBS_ENDPOINT, job_id])

time.sleep(10)

while True:
    response = requests.get(url, headers=headers)

    response_data = response.json()
    status = response_data['status']
    print(f'Job status: {status}')

    if status == 'FINISHED':
        break

    time.sleep(30)

url = ''.join([DOWNLOAD_ENDPOINT, '/net/people/plgrid/plgdawid126/img_1.png0001.png'])
with requests.get(url, headers=headers, stream=True) as r:
    r.raise_for_status()
    with open('./img_1.png0001.png', 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size=8192)):
            f.write(chunk)
