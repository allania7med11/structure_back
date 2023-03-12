import graphene
import graphene_django_extras as extras
from graph.types import IType
from RDM.infs import cst
class CSchema:
    @property
    def fQueries(self):
        data={}
        for k in cst.lstP:
            data[k[:-1]]=extras.DjangoObjectField(IType[k].fType)
            data[k]=extras.DjangoListObjectField(IType[k].fListType)
        return type("Queries",(graphene.ObjectType,),data)

""" class Queries(graphene.ObjectType):
    projects = DjangoListObjectField(ProjectListType, description='All Users query')
    project = DjangoObjectField(ProjectType, description='Single User query')
    nodes = DjangoListObjectField(NodeListType, description='All Users query')
    node = DjangoObjectField(NodeType, description='Single User query')
    supports = DjangoListObjectField(SupportListType, description='All Users query')
    support = DjangoObjectField(SupportType, description='Single User query')
    release = DjangoListObjectField(ReleaseListType, description='All Users query')
    releases = DjangoObjectField(ReleaseType, description='Single User query')
    bar = DjangoListObjectField(BarListType, description='All Users query')
    bars = DjangoObjectField(BarType, description='Single User query') """

schema = graphene.Schema(query=CSchema().fQueries)