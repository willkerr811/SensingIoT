import http.client

conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "9a65ca1584msh65e042d39a9f35cp1b90bajsn21393d526e0a",
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }

conn.request("GET", "/forecast.json?q=Greenwich&days=3", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

'hellop'