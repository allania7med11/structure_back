Production = False
if Production==True:
    database={'NAME': 'postgres','USER': 'postgres','HOST': 'db','PORT': 5432}
    clientUrl="http://localhost"
    cors={"list":[],"app":[],"middleware":[],"session":'Lax'}
else :
    database={'NAME': 'structure_7_2_2020','USER': 'myuser','PASSWORD': 'mypass', 'HOST': 'localhost','PORT': 5432}
    clientUrl="http://localhost:1000"
    cors={
        "list":["http://localhost:1000"],
        "app":["corsheaders"],
        "middleware":['corsheaders.middleware.CorsMiddleware'],
        "session":None}
Test=True
TestInfo= { "user":"user1" }