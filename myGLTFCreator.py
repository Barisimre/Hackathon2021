import struct
import json
from gltflib import FileResource

def get_gltf_file_data(numOfVertices, binFile, textureFile, mins, maxs):

	with open("gltfStructure.json") as json_file:
		data = json.load(json_file)

		bufferByteLength = numOfVertices * 20 # 5 floats * 4 bytes * vertices


		# Add count to accessors
		data["accessors"][0]["count"] = int(numOfVertices)
		data["accessors"][1]["count"] = int(numOfVertices)

		data["accessors"][0]["min"] = mins
		data["accessors"][0]["max"] = maxs

		# Set byte length of buffer in bufferView
		data["bufferViews"][0]["byteLength"] = int(bufferByteLength)

		# Set byte length of buffer
		data["buffers"][0]["uri"] = binFile
		data["buffers"][0]["byteLength"] = int(bufferByteLength)

		# Set image path
		data["images"][0]["uri"] = textureFile

		return data


def getMinMaxOfFaces(faces):

	minX, minY, minZ = faces[0][0][0], faces[0][0][1], faces[0][0][2]
	maxX, maxY, maxZ = faces[0][0][0], faces[0][0][1], faces[0][0][2]

	for face in faces:
		for vertex in face:
			x, y, z = vertex[0], vertex[1], vertex[2]

			if x < minX:
				minX = x
			if x > maxX:
				maxX = x
			if y < minY:
				minY = y
			if y > maxY:
				maxY = y
			if z < minZ:
				minZ = z
			if z > maxZ:
				maxZ = z

	return [minX, minY, minZ], [maxX, maxY, maxZ]


def get_bytearray_from_faces(faces, imageDimension):
	vertex_bytearray = bytearray()


	for face in faces:
		for vertex in face:
			x, y, z = vertex[0], vertex[1], vertex[2]

			# X, y, z
			vertex_bytearray.extend(struct.pack('f', x))
			vertex_bytearray.extend(struct.pack('f', y))
			vertex_bytearray.extend(struct.pack('f', z))
			# tx, ty
			vertex_bytearray.extend(struct.pack('f', x * 100 / imageDimension[0]))
			vertex_bytearray.extend(struct.pack('f', y * 100 / imageDimension[1]))

	return vertex_bytearray


def create_gltf_file(faces, new_bin_file, new_gltf_file, existing_texture_file, imageDimension):
	print("Putting faces in buffer...")
	mins, maxs = getMinMaxOfFaces(faces)

	bytearr = get_bytearray_from_faces(faces, imageDimension)

	print("Creating BIN file... (" + str(len(bytearr)) + " vertices)")
	binFile = FileResource(new_bin_file, data=bytearr)
	binFile.export()

	print("Creating GLTF file...")
	data = get_gltf_file_data(len(bytearr) / 20, new_bin_file, existing_texture_file, mins, maxs)
	with open(new_gltf_file, 'w') as gltfFile:
		json.dump(data, gltfFile)




"""
BIN_FILE = "myVBO.bin"
GLTF_FILE = "myGLTF.gltf"
TEXTURE_FILE = "myTexture.png"

vbo = [
    # Vertices              Texture Coord
    0.0, 0.0, 0.0,          0.0, 0.0,
    1.0, 0.0, 0.0,          1.0, 0.0,
    1.0, 1.0, 1.0,          1.0, 1.0,

    0.0, 0.0, 0.0,          0.0, 0.0,
    1.0, 1.0, 0.0,          1.0, 1.0,
    0.0, 1.0, 0.0,          0.0, 1.0
]

# Add indices to byte array
vertex_bytearray = bytearray()
for value in vbo:
	vertex_bytearray.extend(struct.pack('f', value))

resource = FileResource(BIN_FILE, data=vertex_bytearray)

#resource.export()

#model = GLTFModel(asset=Asset(version='2.0'))
#gltf = GLTF(model=model, resources=[resource])
#gltf.export(GLTF_FILE)
print("Basic shit is set up")

get_gltf_file_text(3, "myVBO.bin", "myTexture.png")

print("Created bin file?")
print("gltf fully set up")
print("Done")
"""
