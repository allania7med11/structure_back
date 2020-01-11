Docker=False
if Docker==True:
    database={'NAME': 'postgres','USER': 'postgres','HOST': 'db','PORT': 5432}
    clientUrl="http://localhost"
    cors={"list":[],"app":[],"middleware":[],"session":'Lax'}
else :
    database={'NAME': 'rdm2','USER': 'myuser','PASSWORD': 'mypass', 'HOST': 'localhost','PORT': 5432}
    clientUrl="http://localhost"
    cors={
        "list":["http://localhost"],
        "app":["corsheaders"],
        "middleware":['corsheaders.middleware.CorsMiddleware'],
        "session":None}
