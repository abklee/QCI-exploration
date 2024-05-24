# Code written to solve the example non-Ising Hamiltonian from page 11 of the Dirac User's Guide

# @author Alex Klee
# @verison 2024.05.24

import qci_client as qc
client = qc.QciClient(
url="https://api.qci-prod.com",
api_token="b81826ebae0f263aaa51e8bb08348ffe",
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
