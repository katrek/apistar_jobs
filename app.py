import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

# Helpers

def load_jobs_data():
    with open('jobs.json') as f:
        jobs = json.loads(f.read())
        return {job["id"]: job for job in jobs}


jobs = load_jobs_data()

JOB_NOT_FOUND = 'Job Not Found'

# Definition

class Job(types.Type):
    id = validators.Integer(allow_null=True) # assign in Post
    first_name = validators.String(max_length=50)
    last_name = validators.String(max_length=50)
    job_title = validators.String(max_length=80)
    company = validators.String(max_length=80)

# API Methods
def list_jobs() -> List[Job]:
    return [Job(job[1]) for job in sorted(jobs.items())]

def create_job(job: Job) -> JSONResponse:
    job_id = len(jobs) + 1
    job.id = job_id
    jobs[job_id] = job
    return JSONResponse(Job(job), status_code=201)

def  get_job(job_id: int) -> JSONResponse:
    job = jobs.get(job_id)
    if not job:
        error = {'error' : JOB_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    return JSONResponse(Job(job), status_code=200)

def update_job(job_id: int, job: Job) -> JSONResponse:
    if not jobs.get(job_id):
        error = {'error' : JOB_NOT_FOUND}
        return JSONResponse(Job(job), status_code=404)
    job.id = job_id
    jobs[job_id] = job
    return JSONResponse(Job(job), status_code=200)

def delete_job(job_id: int) -> JSONResponse:
    if not jobs.get(job_id):
        error = {'error', JOB_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    del jobs[job_id]
    return JSONResponse({}, status_code=204)

routes = [
    Route('/', method='GET', handler=list_jobs),
    Route('/', method='POST', handler=create_job),
    Route('/{job_id}/', method='GET', handler=get_job),
    Route('/{job_id}/', method='PUT', handler=update_job),
    Route('/{job_id}/', method='DELETE', handler=delete_job),

]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)








