import numpy as np
from stl import mesh
from PIL import Image
import glob
import os
from green_screen import green_screen




def threed(im_name, c):



	IMPORT_FILE_IMAGE = im_name
	EXPORT_FILE_MODEL = f"surface_{c}.stl"

	grey_img = Image.open(IMPORT_FILE_IMAGE).convert('RGB')
	# open_cv_image = numpy.array(pil_image) 
	# # Convert RGB to BGR 
	# open_cv_image = open_cv_image[:, :, ::-1].copy() 

	# mask = green_screen(IMPORT_FILE_IMAGE)

	max_size=(500,500)
	max_height=10
	min_height=0

	#height=0 for minPix
	#height=maxHeight for maxPIx

	grey_img.thumbnail(max_size)
	imageNp = np.array(grey_img)
	maxPix=imageNp.max()
	minPix=imageNp.min()

	(ncols,nrows)=grey_img.size

	vertices=np.zeros((nrows,ncols,3))

	for x in range(0, ncols):
		for y in range(0, nrows):			

			pixelIntensity = imageNp[y][x]
			if mask[y][x] == 1:
				z = 0
			else:
				z = (pixelIntensity * max_height) / maxPix
			vertices[y][x]=(x, y, z)

	faces=[]

	for x in range(0, ncols - 1):
		for y in range(0, nrows - 1):
			# create face 1
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

	# print(f"number of faces: {len(faces)}")
	facesNp = np.array(faces)
	# Create the mesh
	surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
	for i, f in enumerate(faces):
			for j in range(3):
					surface.vectors[i][j] = facesNp[i][j]
	# Write the mesh to file "cube.stl"
	surface.save(f"stl/{EXPORT_FILE_MODEL}")
	# print(f"stl/{EXPORT_FILE_MODEL}")



def gen_models():

	files = glob.glob('stl/*.stl', recursive=True)
	for f in files:
		try:
				os.remove(f)
		except OSError as e:
				print('Could not remove the files')

	files = glob.glob('stl/*.stl', recursive=True)
	for f in files:
			try:
					os.remove(f)
			except OSError as e:
					print('Could not remove the files')

	directory = os.fsdecode("img/img_dump")
	# print(os.listdir(directory))

	for f, i in list(zip(os.listdir(directory), range(len(os.listdir(directory))))):
		filename = os.fsdecode(f)
		threed(directory+'/'+filename, i)
gen_models()


