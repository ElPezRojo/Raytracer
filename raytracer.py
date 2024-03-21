import numpy as np
import scene
import sys
import objects
import array as arr

a = sys.argv[0]
class camera:
    eye = [0,0,0]
    at = [0,0,-1]
    
max_passes = 3


input_file = sys.argv[1]

# set up scene and read input file
a, b, c, d = scene.scene.read_file(input_file)
s = scene.scene(a, b, c, d)

# set up viewport 
width, height = s.viewport.resx, s.viewport.resy
w, h = width/2, height/2
near_plane = objects.plane([camera.at[0], camera.at[1], camera.at[2]], 1)

# arrays
final_array = []
rays = np.empty(shape=width * height, dtype=objects.ray)
colour_array = np.empty(width * height, np.ndarray)
c_index = 0


# main raytracing code
def bounce_ray(b_num, r: objects.ray):
    c_obj = None
    i_p = np.array([np.finfo('d').max, np.finfo('d').max, np.finfo('d').max])
    normal = None
    
    # looping through spheres
    for obj in s.object_list:
        obj: objects.sphere
        r: objects.ray
        
        # compute intersection
        temp_int = r.does_intersect(obj)
        if(temp_int is None):
                continue
        elif(np.dot(temp_int, [0,0,-1]) < 0):
                continue
            
        # if the intersection is closer than the closest intersection, save the object and intersection
        if(c_obj is None or (np.linalg.norm(temp_int - camera.eye) < np.linalg.norm(i_p - camera.eye))):
            c_obj = obj   
            i_p = temp_int
            normal = (i_p - c_obj.coords) / c_obj.scale
            normal /= np.linalg.norm(normal)
        else:
            continue
    
    # if nothing has been hit we return the background colour
    if(c_obj is None):
        return s.canvas.b_colour
    
    # new ray that is reflected off of the object
    reflected_ray = objects.ray(i_p, -2 * (np.dot(normal, r.vector)) * normal + r.vector)
    
    # loop through the lights, saving lights that aren't in shadow for later
    lights_not_in_shadow = []
    for l in s.lights:
        l: objects.light
        to_light = objects.ray(i_p, i_p - l.coords)
        
        # loop through objects to see if light souce is blocked
        for obj2 in s.object_list:
            ip = to_light.does_intersect(obj2)
            if(ip is not None):
                continue
            else:
                lights_not_in_shadow.append(l)
                break
    
    ambient_colour = s.canvas.ambient * c_obj.lighting[0] * c_obj.colour
    diffuse_colour = np.zeros(3)
    specular_colour = np.zeros(3)
    
    # loop through lights that aren't in shadow, calculating their respective specular and diffuse contributions
    for l in lights_not_in_shadow:
        
        to_light = (l.coords - i_p - c_obj.coords) / c_obj.scale
        to_light /= np.linalg.norm(to_light)
        dot_p = np.dot(normal, to_light)
        
        # try to not get negative colours
        if(np.dot(normal, to_light) < 0):
            dot_p *= -1
            
        diffuse_colour += l.intensity * c_obj.lighting[1] * c_obj.colour * dot_p
        
        # calculate specular contribution
        h_vector = (to_light - r.vector) 
        normalizer = np.linalg.norm(h_vector)
        if(normalizer > 0):
            h_vector /= normalizer
        bp = np.dot(h_vector, normal)
        specular_colour += (l.intensity * c_obj.lighting[2]) * np.power(bp, obj.n)
        
    
    # recursion control
    if(b_num == max_passes):
        return ambient_colour + diffuse_colour + specular_colour
    else:
        reflected_colour = bounce_ray(b_num + 1, reflected_ray)
        return ambient_colour + diffuse_colour + specular_colour + (reflected_colour * c_obj.lighting[3])
        

# append all rays from eye into the array
rays_index: int = 0
for y in range(height):
    for x in range(width):
        vector = np.array([(-(x - w) / width) * (s.viewport.left - s.viewport.right), (-(y - h) / height) * (s.viewport.top - s.viewport.bottom), (near_plane.non_zero())]) - np.array(camera.eye)
        rays[rays_index] = (objects.ray(camera.eye, vector / np.linalg.norm(vector)))
        rays_index += 1

# do the recursion for each ray
for r in rays:
    col = bounce_ray(1, r)
    colour_array[c_index] = col
    c_index += 1


# clamp the colours proportionally if any are over 1
for c in colour_array:
    while(c[0] > 1 or c[1] > 1 or c[2] > 1):
        c /= 2


# print the end result to a P3 PPM file
header = 'P3\n' +str(width) + ' ' +str(height) + '\n255\n'
f = open(s.canvas.output_name, 'w')
f.write(header)
col_num = 0
row_num = 0

# loop through the pixels, writing the colour of each pixel to the file
for index in range(c_index):
    colour = colour_array[index]
    for ind in colour:
        f.write(str(int(np.rint(255 * ind))) + " ")
    col_num += 1
    if(col_num == width):
        f.write("\n")
        col_num = 0

