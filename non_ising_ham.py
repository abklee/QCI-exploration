# Code written to solve the example non-Ising Hamiltonian from page 11 of the Dirac User's Guide

# @author Alex Klee
# @verison 2024.05.24

import qci_client as qc
client = qc.QciClient(
url="https://api.qci-prod.com",
api_token="SECRET",
)
# polynomial H = -x_1 -2x_2 -3x_3 - x_1^2 + x_2^2 - x_3^2 - 2*x_1*x_2 + 3x_1x_2x_3 - 5x_2x_3 + x_2^2x_3 + x_1^2x_3, subject to x_1 + x_2 + x_3 = 
sum_constraints = [1, 10, 25, 50, 100]
poly_indices = [[0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 1, 1], [0, 2, 2], [0, 3, 3], [0, 1, 2], [1, 2, 3], [0, 2, 3], [2, 2, 3], [1, 1, 3]]
poly_coefficients = [-1, -2, -3, -1, 1, -1, -2, 3, -5, 1, 1]
for s in sum_constraints:
    data = [{"idx": idx, "val": val} for idx, val in zip(poly_indices, poly_coefficients)]
    file = {
    "file_name": "hello-world",
    "file_config": {
    "polynomial": {
    "num_variables": 3,
    "min_degree": 1,
    "max_degree": 3,
    "data": data,
    }
    }
    }
    file_response = client.upload_file(file=file)

    job_body = client.build_job_body(
    job_type='sample-hamiltonian',
    job_params={'device_type': 'dirac-3', 'relaxation_schedule': 2, 'sum_constraint': s, 'solution_precision': 1},
    polynomial_file_id=file_response['file_id'],
    )
    job_response = client.process_job(job_body=job_body)
    assert job_response["status"] == qc.JobStatus.COMPLETED.value
    print(
    f"Result [x_1, x_2, x_3] = {job_response['results']['solutions'][0]} is " + 
    ("optimal" if job_response["results"]["energies"][0] == -1 else "suboptimal") +
    f" with H = {job_response['results']['energies'][0]}"
    )
'''
Output:

2024-05-24 12:21:49 - Dirac allocation balance = 2802 s
2024-05-24 12:21:49 - Job submitted: job_id='6650be9ca3e6a645a5c4d4e5'
2024-05-24 12:21:49 - QUEUED
2024-05-24 12:21:51 - RUNNING
2024-05-24 12:21:59 - COMPLETED
2024-05-24 12:22:02 - Dirac allocation balance = 2797 s
Result [x_1, x_2, x_3] = [0, 0.1756214, 0.8243786] is suboptimal with H = -4.1716018
2024-05-24 12:22:03 - Dirac allocation balance = 2797 s
2024-05-24 12:22:04 - Job submitted: job_id='6650beaba3e6a645a5c4d4e6'
2024-05-24 12:22:04 - QUEUED
2024-05-24 12:22:06 - RUNNING
2024-05-24 12:22:12 - COMPLETED
2024-05-24 12:22:14 - Dirac allocation balance = 2792 s
Result [x_1, x_2, x_3] = [0, 1.084118, 8.9158821] is suboptimal with H = -145.0839233
2024-05-24 12:22:16 - Dirac allocation balance = 2792 s
2024-05-24 12:22:16 - Job submitted: job_id='6650beb7a3e6a645a5c4d4e7'
2024-05-24 12:22:16 - QUEUED
2024-05-24 12:22:19 - RUNNING
2024-05-24 12:22:24 - COMPLETED
2024-05-24 12:22:26 - Dirac allocation balance = 2787 s
Result [x_1, x_2, x_3] = [0, 1.3199333, 23.6800671] is suboptimal with H = -747.7080078
2024-05-24 12:22:28 - Dirac allocation balance = 2787 s
2024-05-24 12:22:28 - Job submitted: job_id='6650bec3a3e6a645a5c4d4e8'
2024-05-24 12:22:28 - QUEUED
2024-05-24 12:22:31 - RUNNING
2024-05-24 12:22:36 - COMPLETED
2024-05-24 12:22:39 - Dirac allocation balance = 2782 s
Result [x_1, x_2, x_3] = [49.7571182, 0.2428803, 0] is suboptimal with H = -2550.125
2024-05-24 12:22:40 - Dirac allocation balance = 2782 s
2024-05-24 12:22:40 - Job submitted: job_id='6650bed0a3e6a645a5c4d4e9'
2024-05-24 12:22:40 - QUEUED
2024-05-24 12:22:43 - RUNNING
2024-05-24 12:22:48 - COMPLETED
2024-05-24 12:22:51 - Dirac allocation balance = 2777 s
Result [x_1, x_2, x_3] = [0, 1.3673675, 98.632637] is suboptimal with H = -10515.0820312
'''

