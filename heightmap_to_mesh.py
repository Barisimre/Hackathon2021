import numpy as np
from stl import mesh
from PIL import Image
import glob
import os




def get_stl(gray, background):

	max_size=(500,500)
	max_height=10
	min_height=0

	maxPix = 255

	vertices = np.zeros((len(gray), len(gray[0]), 3))
	# Get vertices from heightmap
	for y in range(len(gray)):
		for x in range(len(gray[0])):
			intensity = gray[y][x]
			z = (intensity * max_height) / maxPix
			vertices[y][x] = (x, y, z)


	# Get faces from vertices that are not baackground
	faces = []
	for y in range(len(gray)-1):
		for x in range(len(gray[0])-1):
			#Make square of 2 triangles

			if background[y][x] == 0:

				vertice1 = vertices[y][x]
				vertice2 = vertices[y+1][x]
				vertice3 = vertices[y+1][x+1]
				face1 = np.array([vertice1,vertice2,vertice3])

				# create face 2
				vertice1 = vertices[y][x]
				vertice2 = vertices[y][x+1]
				vertice3 = vertices[y+1][x+1]

				face2 = np.array([vertice1,vertice2,vertice3])

				faces.append(face1)
				faces.append(face2)
	
	# Convert faces into mesh
	facesNp = np.array(faces)
	# Create the mesh
	surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
	for i, f in enumerate(faces):
			for j in range(3):
					surface.vectors[i][j] = facesNp[i][j]
	# Write the mesh to file "cube.stl"


	export_file = f"stl/stlFile.stl"
	surface.save(export_file)
	# print(f"stl/{EXPORT_FILE_MODEL}")
	return export_file



