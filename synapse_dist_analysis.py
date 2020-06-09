import numpy as np
import os
import math
import matplotlib.pyplot as plt
import seaborn as sns


def main(input_file, scale_factor=1):

    verts, faces = read_obj(input_file)
    path, file_name = os.path.split(input_file)

    #This scale factor moves us from the pixel dimension to microns
    verts = verts * scale_factor

    visited_verts = set()
    islands = []

    for vert_index, vert in enumerate(verts):
        if vert_index not in visited_verts:
            current_island = find_island(vert_index, verts, faces)
            islands.append(list(current_island))
            for part in current_island:
                visited_verts.add(part)


    island_centers = []

    for island in islands:
        x_total = 0.0
        y_total = 0.0
        z_total = 0.0
        count = 0
        for vert in island:
            x_total += verts[vert][0]
            y_total += verts[vert][1]
            z_total += verts[vert][2]
            count += 1
        x_average = x_total / count
        y_average = y_total / count
        z_average = z_total / count

        island_centers.append([x_average, y_average, z_average])

    print("Number of separate components: " + str(len(island_centers)))

    shortest_dists = []
    for island_center_index, island_center_coords in enumerate(island_centers):
        dist, index = nearest_neighbor(island_center_index, island_centers)
        shortest_dists.append(dist)

    """
    Histogram settings here
    """
    max_value = 2.5
    min_value = 0.0
    bin_width = 0.1

    sns.set_style("darkgrid")
    plt.figure(figsize=(8,6))
    ax = sns.distplot(shortest_dists,
                      bins=int((max_value-min_value)/bin_width),
                      hist_kws={'range': (min_value, max_value)},
                      kde=False,
                      rug=True,
                      norm_hist=False)

    ax.set(xlabel='Distance (microns)', ylabel="Count", title=file_name)
    plt.text(1.7, 2.3, "Count: " + str(len(island_centers)), fontsize=12)

    figure = ax.get_figure()
    output_filename = file_name + "_distributionHist.png"
    figure.savefig(output_filename, dpi=300)


def nearest_neighbor(point_index, points):
    """
    return the nearest neighbor index and distance
    :param point_index: starting point
    :param points: a 2-d list where each row is a new point and the column correspond to x, y, z, coordinates
    :return:
    """
    nearest_distance = 9999
    nearest_index = -1
    x_coord = points[point_index][0]
    y_coord = points[point_index][1]
    z_coord = points[point_index][2]
    for point, coordinates in enumerate(points):
        if point == point_index:
            pass
        else:
            x_dist = abs(x_coord - coordinates[0])
            y_dist = abs(y_coord - coordinates[1])
            z_dist = abs((z_coord - coordinates[2]))

            distance = math.sqrt(x_dist**2 + y_dist**2 + z_dist**2)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_index = point

    return(nearest_distance, nearest_index)


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


main("/home/user1/Synapse_Distribution/test_files/VCN_c30_SinputTerminal04_Synapses_deci.obj", scale_factor=0.011)

