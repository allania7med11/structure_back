qProject='''
query project($id: ID!) {
  project(id: $id) {
    id,name,
    nodes {project{id},id,name,X,Z,Support{name},N1{name},N2{name}}
    supports {project{id},id,name,UX,UZ,RY,nodes{id,name}}
    bars{project{id},id,name,N1{id,name,X,Z},N2{id,name,X,Z},Release{name}} 
    releases{project{id},id,name,UX1,UZ1,RY1,UX2,UZ2,RY2,bars{id,name}},
  }
  default:project(id: 1) {
    id,name
    supports {project{id},id,name,nodes(project: $id){id,name} }
    releases{project{id},id,name,UX1,UZ1,RY1,UX2,UZ2,RY2,bars(project: $id){id,name}},
  }
}
'''
