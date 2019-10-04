import graphene
from graph.schema import Qr

class Query(Qr,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
