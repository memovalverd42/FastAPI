import requests

url = 'http://127.0.0.1:8000/api/v1/reviews'

response = requests.get(url)

if response.status_code == 200:
    print('peticion exitosa')