# Code written to solve the example ising hamiltonian from page 9 of the Dirac User's Guide

# @author Alex Klee
# @verison 2024.05.23

import numpy as np
from qci_client import QciClient
import os

token = "b81826ebae0f263aaa51e8bb08348ffe"
api_url = "https://api.qci-prod.com"
qclient = QciClient(api_token=token, url=api_url)

J = np.array([[-5, 2, 4, 0], [2, -3, 1, 0], [4, 1, -8, 5], [0, 0, 5, -6]]) 
C = np.array([1, 2, 3, 4])

n = C.shape[0]
H = np.hstack([C.reshape([n, 1]), J])

ising_ham_data = {
    'file_name': "ising_ham_example.json",
    'file_config': {'hamiltonian':{"data": H}}
}

response_json = qclient.upload_file(file=ising_ham_data)

job_body = qclient.build_job_body(job_type="sample-hamiltonian-ising",
    hamiltonian_file_id=response_json['file_id'],
    job_params={"device_type": "dirac-1", "num_samples": 1})

print(job_body)

job_response = qclient.process_job(job_body=job_body,verbose=True)

print(job_response)