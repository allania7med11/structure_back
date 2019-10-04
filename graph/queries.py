qProject='''
query project($id: ID!) {
  project(id: $id) {
    id
    name
    nodes {
      name
    }
    supports {
      project{id}
      name
      nodes(project: $id) {
        project {
          name
        }
        name
        id
      }
    }
  }
  default:project(id: 1) {
    id
    name
    supports {
      project{id}
      name
      nodes(project: $id) {
        project {
          name
        }
        name
        id
      }
    }
  }
}
'''
