import numpy as np
import sys


def main(input_file):

    verts, faces = read_obj(input_file)
    island_1 = find_island(0, verts, faces)
    print(island_1)
    island_2 = find_island(8, verts, faces)
    print(island_2)




def find_island(vert_index, verts, faces, island=set(), starting_var=True):
    """
    takes in a vertex and returns all vertices connected, in other words finds
    one disconnected component
    :param vert_index: seed index
    :param verts: list of all verts
    :param faces: list of all faces
    :param island: set of all vertices
    :param starting_var: only true on first run, after it will be set to False
            there is probably a cleaner way of doing this, I just do not know it
    :return: island - set of all vertices
    """
    if starting_var:
        island.clear()

    island.add(vert_index)
    connected_faces = find_connected_faces(vert_index, faces)
    for face in connected_faces:
        #print(faces[face][0])
        if faces[face][0] not in island:
            island.add(faces[face][0])
            find_island(faces[face][0], verts, faces, island=island, starting_var=False)
        if faces[face][1] not in island:
            island.add(faces[face][1])
            find_island(faces[face][1], verts, faces, island=island, starting_var=False)
        if faces[face][2] not in island:
            island.add(faces[face][2])
            find_island(faces[face][2], verts, faces, island=island, starting_var=False)

    return(island)


def find_connected_faces(vert_index, faces):
    """
    Find all faces connected to a specific vertex
    :param vert_index: The index of the vertex to be located
    :param faces: list of all faces
    :return: all faces connected to the starting vertex (vert_index)
    """

    row_indices, col_indices = np.where(faces == vert_index)

    return(row_indices)


def read_obj(in_file):

    with open(in_file) as f:
        mylist = f.read().splitlines()

    verts = []
    faces = []

    for line in mylist:
        if line.startswith("f") or line.startswith("v"):
            split_line = line.split(" ")

            if split_line[0] == 'v':
                verts.append(split_line[1:])
            elif split_line[0] == 'f':
                raw_face = split_line[1:]
                face = []
                for element in raw_face:
                    face.append(int(element.split("/")[0]))
                faces.append(face)

    verts_array = np.array(verts, dtype=float)
    faces_array = np.array(faces, dtype=int)
    # The faces index verts beginning at 1
    # we need it to start at 0 to be the index of vert array

    faces_array = faces_array - 1

    return(verts_array, faces_array)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('error')

