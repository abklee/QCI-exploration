import qci_client as qc
client = qc.QciClient(
url="https://api.qci-prod.com",
api_token="SECRET",
)
# polynomial H = -x_1^2 + 2*x_1*x_2 - x_2^2, subject to x_1 + x_2 = 1, x_1>=0, x_2>=0.
poly_indices = [[1, 1], [1, 2], [2, 2]]
poly_coefficients = [-1, 2, -1]
data = [{"idx": idx, "val": val} for idx, val in zip(poly_indices, poly_coefficients)]
file = {
"file_name": "hello-world",
"file_config": {
"polynomial": {
"num_variables": 2,
"min_degree": 2,
"max_degree": 2,
"data": data,
}
}
}

file_response = client.upload_file(file=file)

job_body = client.build_job_body(
job_type='sample-hamiltonian',
job_params={'device_type': 'dirac-3', 'relaxation_schedule': 1, 'sum_constraint': 1},
polynomial_file_id=file_response['file_id'],
)
job_response = client.process_job(job_body=job_body)
assert job_response["status"] == qc.JobStatus.COMPLETED.value
print(
f"Result [x_1, x_2] = {job_response['results']['solutions'][0]} is " + 
("optimal" if job_response["results"]["energies"][0] == -1 else "suboptimal") +
f" with H = {job_response['results']['energies'][0]}"
)
