import httpx

print('------------------------------------------------')
body = {
    "email": "magregar@example.com",
    "password": "12345"
}
response = httpx.post('http://127.0.0.1:8000/api/v1/authentication/login', json=body)
accessToken = response.json()['token']['accessToken']
print(f'accessToken - {response.json()['token']['accessToken']}'
      f'\nrefreshToken - {response.json()['token']['refreshToken']}'
      f'\nстатус код ответа - {response.status_code}'
)

print('------------------------------------------------')
headers = {"accept": "application/json", "Authorization": f"Bearer {accessToken}"}
print(f'Заголовки запроса - {headers}')

response_get_users_me = httpx.get('http://127.0.0.1:8000/api/v1/users/me', headers=headers)
print('------------------------------------------------')
print(f'Ответ сервера - {response_get_users_me.json()}'
      f'\nстатус код ответа - {response_get_users_me.status_code}')
