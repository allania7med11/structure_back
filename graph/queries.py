qProject='''
query project($id: ID!) {
  project(id: $id) {
    id,name,
    nodes {project{id},id,name,X,Z,Support{name},N1{name},N2{name}}
    supports {project{id},id,name,UX,UZ,RY,nodes{id,name}}
    bars{project{id},id,name,N1{id,name,X,Z},N2{id,name,X,Z},Release{name}} 
    releases{project{id},id,name,UX1,UZ1,RY1,UX2,UZ2,RY2,bars{id,name}},
    materials{project{id},id,name,YM,Density}
    sections{project{id},id,name,material{id,name},type,features,bars{id,name},Ax,Iy,H,Cy},
  }
  default:project(id: 1) {
    id,name
    supports {project{id},id,name,UX,UZ,RY,nodes(project: $id){id,name} }
    releases{project{id},id,name,UX1,UZ1,RY1,UX2,UZ2,RY2,bars(project: $id){id,name}},
    materials{project{id},id,name,YM,Density}
    sections{project{id},id,name,material{id,name},type,features,bars(project: $id){id,name},Ax,Iy,H,Cy},
  }
}
'''


def qApply(name,apply):
    rtn='''
      query {0}($id: ID!,$idU: ID!) [
        {0}(id: $id) [
          project[name],id,name,{1}(project_User: $idU)[project[name],id,name]
        ]
      ]
      '''.format(name,apply).replace("[","{").replace("]","}")
    print(rtn)
    return rtn
