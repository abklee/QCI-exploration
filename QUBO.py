# Code written to solve the example QUBO from page 7 of the Dirac User's Guide

# @author Alex Klee
# @verison 2024.05.23

import numpy as np
from qci_client import QciClient
import os

token = "b81826ebae0f263aaa51e8bb08348ffe"
api_url = "https://api.qci-prod.com"
qclient = QciClient(api_token=token, url=api_url)

Q = np.array([[-5, 2, 4, 0], [2, -3, 1, 0], [4, 1, -8, 5], [0, 0, 5, -6]]) 

qubo_data = {
    'file_name': "qubo_example.json",
    'file_config': {'qubo':{"data": Q}}
}

response_json = qclient.upload_file(file=qubo_data)

job_body = qclient.build_job_body(job_type="sample-qubo",
    qubo_file_id=response_json['file_id'],
    job_params={"device_type": "dirac-1", "num_samples": 5})

print(job_body)

job_response = qclient.process_job(job_body=job_body,verbose=True)

print(job_response)