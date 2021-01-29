from vec3 import Vec3
import color
import sys

image_width = 256
image_height = 256
print('P3\n%d %d\n255\n' % (image_width, image_height))

for j in range(image_height - 1, -1, -1):
    sys.stderr.write('\rScanlines remaining: %d'% j)
    for i in range(0, image_width, 1):
        col = Vec3(i/(image_width-1), j/(image_height-1), 0.25)
        color.write_color(col)

print('accomplished!')

