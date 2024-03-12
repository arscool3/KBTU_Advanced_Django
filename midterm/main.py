# Job site

# job -> title, salary, time, experience, employer, skills, candidates,
# employer -> name, location, jobs
# candidate -> name, education, experience, location,  jobs (applied)
# skill -> title, candidates, jobs

# try yield finally


from fastapi import FastAPI
import database as db
import models
import schemas
app = FastAPI()


@app.get('/employers')
def get_employers():
    pass


@app.post('/employers')
def add_employer(employer: schemas.CreateEmployer):
    db.session.add(models.Employer(**employer.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{employer.name} was added"


@app.post('/jobs')
def add_job(job: schemas.CreateJob):
    db.session.add(models.Job(**job.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{job.title} was added"


@app.post('/candidates')
def add_candidate(candidate: schemas.CreateCandidate):
    db.session.add(models.Candidate(**candidate.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{candidate.name} was added"


@app.get('/candidates')
def get_candidate_by_id(id: int):
    db_candidate = db.session.get(models.Candidate, id)
    candidate = schemas.Candidate.model_validate(db_candidate)
    return candidate


@app.post('/skills')
def add_skill(skill: schemas.CreateSkill):
    db.session.add(models.Skill(**skill.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{skill.title} was added"


@app.get('/skills')
def get_skill_by_title(title: str):
    db_skill = db.session.query(models.Skill).filter(models.Skill.title == title).first()
    skill = schemas.Skill.model_validate(db_skill)
    return skill


@app.post('/candidates/skills')
def add_skill_to_candidate(candidate_id: int, skill_title: str):
    db_candidate = db.session.get(models.Candidate, candidate_id)
    db_skill = db.session.query(models.Skill).filter(models.Skill.title == skill_title).first()

    db_candidate.skills.append(db_skill)
    db_skill.candidates.append(db_candidate)
    candidate = schemas.Candidate.model_validate(db_candidate)
    db.session.commit()
    db.session.close()
    return f"{skill_title} was added to candidate: {candidate.name}"


@app.get('/candidates/skills')
def get_candidate_skills(candidate_id: int):
    db_candidate = db.session.get(models.Candidate, candidate_id)
    candidate = schemas.Candidate.model_validate(db_candidate)
    db_skills = db_candidate.skills
    skills = [schemas.Skill.model_validate(skill) for skill in db_skills]
    return f"{candidate.name}'s skills: {skills}"


@app.post('/candidates/jobs')
def add_skill_to_candidate(candidate_id: int, job_id: int):
    db_candidate = db.session.get(models.Candidate, candidate_id)
    db_job = db.session.get(models.Job, job_id)

    db_candidate.jobs.append(db_job)
    db_job.candidates.append(db_candidate)

    candidate = schemas.Candidate.model_validate(db_candidate)
    job = schemas.Job.model_validate(db_job)
    db.session.commit()
    db.session.close()
    return f"{candidate.name} applied to the job: {job.title}"


@app.get('/candidates/jobs')
def get_candidate_skills(candidate_id: int):
    db_candidate = db.session.get(models.Candidate, candidate_id)
    candidate = schemas.Candidate.model_validate(db_candidate)
    db_jobs = db_candidate.jobs
    jobs = [schemas.Job.model_validate(job) for job in db_jobs]
    return f"Jobs that is {candidate.name} applied: {jobs}"


@app.post('/jobs/skills')
def add_skill_to_job(job_id: int, skill_title: str):
    db_job = db.session.get(models.Job, job_id)
    db_skill = db.session.query(models.Skill).filter(models.Skill.title == skill_title).first()
    db_skill.jobs.append(db_job)
    db_job.skills.append(db_skill)
    job = schemas.Job.model_validate(db_job)
    db.session.commit()
    db.session.close()
    return f"{skill_title} was added to candidate: {job.title}"


@app.get('/jobs/skills')
def get_job_skills(job_id: int):
    db_job = db.session.get(models.Job, job_id)
    job = schemas.Job.model_validate(db_job)
    db_skills = db_job.skills
    skills = [schemas.Skill.model_validate(skill) for skill in db_skills]
    return f"Skills that is {job.title} required: {skills}"

