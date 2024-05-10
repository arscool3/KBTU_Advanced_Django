{
  "amount": 2,
  "x": 1,
  "y": 3
}
for rn to run the app:
1) start the db
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres
alembic revision -m 'initial_migration' --autogenerate
alembic upgrade head
2) make sure u hve redis running
#docker run -d --name redis -p 6379:6379 redis/redis-stack-server:latest
3) 
fastapi uvicorn sqlalchemy graphene graphene-sqlalchemy alembic psycopg2 black python-dotenv
4)start the main app 
(venv) PS C:\Users\Админ\Desktop\adv backend\fast> uvicorn main:app --reload
5) start the  dramatiq
PS C:\Users\Админ\Desktop\adv backend\fast\dramatiq_job> dramatiq main
6) start the test server on a separate port
(venv) PS C:\Users\Админ\Desktop\adv backend\fast\test_server> uvicorn main:app --reload --port 9000      


alembic init alembic

docker-compose run app alembic revision --autogenerate -m "New Migration" docker-compose run app alembic upgrade head
DOCKER-COMPOSE BUILD
DOCUKE

mutation CreateNewPost{ createNewPost(title:"new title1", content:"new content") { ok } }
UVICORN MAIN
query{ allPosts{ title } }

query{ postById(postId:2){ id title content } }

mutation newuser{ createNewUser(username:"test1", password:"test1") { ok } }

mutation authenticateUser{ authenticateUser(username:"test10", password:"test10") { ok } }

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidGVzdDEiLCJleHAiOjE2MjU1OTIyMDB9.4EaNBwe3yjg9NjwcC5F5S0zFaAr_QiOSTTGXjJqFHdk

mutation CreateNewPost{ createNewPost(title:"new title1", content:"new content", token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidGVzdDIwIiwiZXhwIjoxNjI1Njc4MzA1fQ.bUxdKz1KWougGZw-vRLdBGZN87WloCg-6Rai-bCObAc") { result } }