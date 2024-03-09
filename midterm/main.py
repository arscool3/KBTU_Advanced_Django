# Job site

# job -> title, salary, time, experience, employer, skills, candidates,
# employer -> name, location, jobs
# candidate -> name, education, experience, location,  jobs (applied)
# skill -> title, candidates, jobs


from fastapi import FastAPI

app = FastAPI()

app.get('employers')
def get_employers():
    pass