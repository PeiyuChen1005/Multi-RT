from vec3 import Vec3

def write_color(pixel_color:Vec3):
    ir = int(255.999 * pixel_color.x)
    ig = int(255.999 * pixel_color.y)
    ib = int(255.999 * pixel_color.z)
    print(ir, ' ', ig, ' ', ib, '\n')
