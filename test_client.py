import requests

data = {'email': 'nelsonatuti20@gmail.com', 'password': '1234'}

response = requests.post('http://127.0.0.1:8000/jwt/create', data=data)
try:
    accessToken = response.json()['access']
    if accessToken:
        headers = {
            # "Authorization": f"Bearer {accessToken}"
        }
        response2 = requests.post("http://127.0.0.1:8000/mark/register", headers=headers)
        print(response2.json())
except:
    print(response.json())

