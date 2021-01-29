import sys
image_width = 256
image_height = 256
print('P3\n%d %d\n255\n' % (image_width, image_height))

for j in range(image_height - 1, -1, -1):
    sys.stderr.write('\rScanlines remaining: %d'% j)
    for i in range(0, image_width, 1):
        r = i / (image_width - 1)
        g = j / (image_height - 1)
        b = 0.25

        ir = int(255.999 * r)
        ig = int(255.999 * g)
        ib = int(255.999 * b)
        print('%d %d %d' % (ir, ig, ib))

print('accomplished!')
