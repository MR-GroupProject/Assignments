# import mindboggle.shapes.zernike.zernike as zernike
# import numpy as np
# import json

# file_path_list = open("file_path_json.txt", 'r')

# for fp in file_path_list:

#     file_path = fp.strip('\n')

#     file = open(file_path, 'r')

#     json_file = json.load(file)

#     points = json_file["vertices"]
#     faces = json_file["triangles"]

#     moments = zernike.zernike_moments(
#         points=points,
#         faces=faces,
#         order=3,
#         scale_input=False,
#         decimate_fraction=0,
#         decimate_smooth=0,
#         verbose=False)
