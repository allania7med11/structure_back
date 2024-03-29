class cQueries:
    project = '''
		query project($id: ID!) {
			project(id: $id) {
				id,name,results,
				nodes {project{id},id,name,X,Z,Support{name},pls{name},N1{name},N2{name},Rc,Dp}
				supports {project{id},id,name,UX,UZ,RY,nodes{id,name}}
				bars{project{id},id,name,N1{id,name,X,Z},N2{id,name,X,Z},Release{name},Section{name,type},dls{name,type},L,Rl,Rg,Ql,Qg,EF,DP,S,EFm,DPm,Sm} 
				releases{project{id},id,name,UX1,UZ1,RY1,UX2,UZ2,RY2,bars{id,name}},
				materials{project{id},id,name,YM,Density}
				sections{project{id},id,name,material{id,name},type,features,bars{id,name},Ax,Iy,H,Cy},
				pls{project{id},id,name,FX,FZ,CY,nodes{id,name}}
				dls{project{id},id,name,type,Axes,features,bars{id,name}}
			}
			default:project(id: 1) {
				id,name
				supports {project{id},id,name,UX,UZ,RY,nodes(project: $id){id,name} }
				releases{project{id},id,name,UX1,UZ1,RY1,UX2,UZ2,RY2,bars(project: $id){id,name}},
				materials{project{id},id,name,YM,Density}
				sections{project{id},id,name,material{id,name},type,features,bars(project: $id){id,name},Ax,Iy,H,Cy},
			}
		}'''
    copy = '''
		query project($id: ID!) {
			project(id: $id) {
				supports {name,UX,UZ,RY}
				releases{name,UX1,UZ1,RY1,UX2,UZ2,RY2},
				materials{name,YM,Density}
				sections{name,material{name},type,features},
				nodes {name,X,Z,Support{name}}
				bars{name,N1{name},N2{name},Release{name},Section{name}}
				pls{name,FX,FZ,CY,nodes{id,name}}
				dls{name,type,Axes,features,bars{id,name}}
				} 
			}'''
    results = '''
		query project($id: ID!) {
			project(id: $id) {
				id,name,
				nodes {id,name,Rc,Dp}
				bars{id,name,N1{id,name},N2{id,name},L,Rl,Rg,Ql,Qg,EF,DP,S,EFm,DPm,Sm} 
				sections{id,name,Ax,Iy,H,Cy,bars{id,name}},
			}
			default:project(id: 1) {
				id,name
				sections{id,name,Ax,Iy,H,Cy,bars(project: $id){id,name}},
			}}'''
    def apply(self, name, apply):
        rtn = '''
			query {0}($id: ID!,$idU: ID!) [
				{0}(id: $id) [
				project[name],id,name,{1}(project_User: $idU)[project[name],id,name]
				]
			]'''.format(name, apply).replace("[", "{").replace("]", "}")
        return rtn


Queries = cQueries()
