import http.client

conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6d1442a489mshccb38dca71d2ca5p12253ajsndc8acfc924bb",
    'x-rapidapi-host': "linkedin-data-api.p.rapidapi.com"
}

conn.request("GET", "/?username=adamselipsky", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))