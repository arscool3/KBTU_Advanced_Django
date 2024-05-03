import dramatiq
import requests

@dramatiq.actor
def factorial(n: int):
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    print(fact)

@dramatiq.actor
def perehvat():
    response = requests.get('http://127.0.0.1:8000/leagues')
    print(response.json())