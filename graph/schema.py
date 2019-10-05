import graphene
from graphene_django_extras import DjangoListObjectField,DjangoObjectField
from graph.types import ProjectListType,ProjectType,NodeListType,NodeType,SupportListType,SupportType,BarListType,BarType,ReleaseListType,ReleaseType

class Queries(graphene.ObjectType):
    projects = DjangoListObjectField(ProjectListType, description='All Users query')
    project = DjangoObjectField(ProjectType, description='Single User query')
    nodes = DjangoListObjectField(NodeListType, description='All Users query')
    node = DjangoObjectField(NodeType, description='Single User query')
    supports = DjangoListObjectField(SupportListType, description='All Users query')
    support = DjangoObjectField(SupportType, description='Single User query')
    release = DjangoListObjectField(ReleaseListType, description='All Users query')
    releases = DjangoObjectField(ReleaseType, description='Single User query')
    bar = DjangoListObjectField(BarListType, description='All Users query')
    bars = DjangoObjectField(BarType, description='Single User query')

schema = graphene.Schema(query=Queries)