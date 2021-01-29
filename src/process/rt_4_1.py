from vec3 import Vec3
from ray import  Ray
import color
import sys

def ray_color(r:Ray):
    unit_direction = Vec3.unit_vector(r.direction)
    # 混合
    t = 0.5*(unit_direction.y+1.0)
    return (1.0-t)*Vec3(1.0,1.0,1.0)+t*Vec3(0.5,0.7,1.0)

aspect_ratio = 16.0/9.0
# height/width
image_width = 400
image_height = int(image_width/aspect_ratio)

viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0

origin = Vec3(0,0,0)
horizontal = Vec3(viewport_width,0,0)
vertical = Vec3(0,viewport_height,0)
lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0,0,focal_length)

print('P3\n%d %d\n255\n' % (image_width, image_height))

for j in range(image_height - 1, -1, -1):
    sys.stderr.write('\rScanlines remaining: %d' % j)
    for i in range(0, image_width, 1):
        u = i/(image_width-1)
        v = j/(image_height-1)

        r = Ray(origin, lower_left_corner+u*horizontal+v*vertical-origin)

        pixel_color = ray_color(r)
        color.write_color(pixel_color)