import gmsh

###############################################
###### CREATE EXAMPLE SURFACE MESH FROM CAD MODEL ######
###############################################

# LOAD CAD AND INITIALIZE MESH

gmsh.initialize()
gmsh.option.setString(
    "Geometry.OCCTargetUnit", "M"
)  # make sure gmsh reads .step file in meters
gmsh.model.add("inlet_mesh")

cad_file_path = "chap_2/cylinder.step"

entities = gmsh.model.occ.importShapes(cad_file_path)
gmsh.model.occ.synchronize()

# EXTRACT ALL VOLUMES
volumes = [e for e in gmsh.model.occ.getEntities() if e[0] == 3]

print(f"Extracted {len(volumes)} raw volumes from CAD.")

# volumes info for debugging
for v in volumes:
    com = gmsh.model.occ.getCenterOfMass(v[0], v[1])
    bbox = gmsh.model.getBoundingBox(v[0], v[1])

##### TAG & NAME PHYSICAL GROUPS #####
# volumes
gmsh.model.addPhysicalGroup(3, [1], 1, name=f"volume")

# surfaces
inlet = 2
walls = 1
outlet = 3

gmsh.model.addPhysicalGroup(2, [inlet], 2, name="inlet")
gmsh.model.addPhysicalGroup(2, [outlet], 3, name="outlet")
gmsh.model.addPhysicalGroup(2, [walls], 4, name="walls")

##### MESH SIZE & REFINEMENT #####
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 20)

# for quad mesh
gmsh.option.setNumber("Mesh.Algorithm", 8)   
gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 3) 
gmsh.option.setNumber("Mesh.Recombine3DAll", 1) 

##### SYNC & GENERATE MESH #####
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)

##### SAVE MESH #####
output_file = "chap_2/inlet_quad_mesh.msh"
gmsh.write(output_file)
gmsh.finalize()