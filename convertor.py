import os


def convert_ply_into_off(input_file):
    f_name = os.path.splitext(input_file)[0]
    print(f_name)
    output_file = os.path.join(f_name + '.off')
    f_output = open(output_file, "w")
    f_output.write('OFF\n')
    end_header = False
    v, f = '0', '0'
    f_input = open(input_file)
    for i, line in enumerate(f_input):
        if line.startswith('element vertex'):
            v = line.split(' ')[2]
        elif line.startswith('element face'):
            f = line.split(' ')[2]
        elif line.strip() == 'end_header':
            end_header = True
            f_output.write('{} {} {}\n'.format(v.strip(), f.strip(), '0'))

        if end_header and line.strip() != 'end_header':
            f_output.write(line)

    f_output.close()
    return output_file

# test
# convent_ply_into_off("./PLY/ant.ply")
