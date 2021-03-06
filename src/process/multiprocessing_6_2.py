from vec3 import Vec3
from ray import Ray
from hitable import Hitable,HitableList,Sphere
import sys
from camera import Camera
import multiprocessing as mp
import random
import time

# image
aspect_ratio = 16.0 / 9.0  # height/width
image_width = 160
image_height = int(image_width / aspect_ratio)
sample_per_pixel = 100
# camera
viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0
ori = Vec3(0, 0, 0)
hor = Vec3(viewport_width, 0, 0)
ver = Vec3(0, viewport_height, 0)
llc = ori - hor / 2 - ver / 2 - Vec3(0, 0, focal_length)
cam = Camera(ori, hor, ver, llc)
# world
world = HitableList([Sphere(Vec3(0, 0, -1), 0.5), Sphere(Vec3(0, -100.5, -1), 100)])

def ray_color(r : Ray, world : Hitable):
    hit_rec =world.hit(r, 0, sys.float_info.max)
    if hit_rec:
        return 0.5*(hit_rec.normal + Vec3(1,1,1)) # modified to [0,1)
    unit_direction = Vec3.unit_vector(r.direction)
    # 混合
    t = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)
def color_block(coordinate, t_num,block):#从左上角向右下角计算  ul_x,ul_y,lr_x,lr_y
    for j in range(coordinate[1] - 1, coordinate[3]-1, -1):
        remaining_line=j-coordinate[3]
        sys.stderr.write('\rScanlines remaining: %d \n' % remaining_line)
        sys.stderr.write('\rThread number: %d \n' % t_num)
        for i in range(coordinate[0], coordinate[2], 1):
            pixel_color = Vec3(0,0,0)
            for s in range(sample_per_pixel):
                u = (i+random.random()) / (image_width - 1)
                v = (j+random.random()) / (image_height - 1)
                r = cam.get_ray(u, v)
                pixel_color += ray_color(r, world)
            pixel_color /= sample_per_pixel
            ir = int(255.999 * pixel_color.x)
            ig = int(255.999 * pixel_color.y)
            ib = int(255.999 * pixel_color.z)
            block.append(ir)
            block.append(ig)
            block.append(ib)

if __name__ == '__main__':
    blocks=[]
    process_cnt = 8
    with mp.Manager() as MG:
        # color block
        for i in range(process_cnt):
           blocks.append(mp.Manager().list([]))

    st = time.time()
    #coordinates
    coordinates = []
    for i in range(process_cnt):
        coordinates.append([0, int((1-i/process_cnt)*image_height), image_width, int((1-(i+1)/process_cnt)*image_height)])
    print(coordinates)
    #result
    processes = []

    for i in range(process_cnt):
        p = mp.Process(target=color_block, args=(coordinates[i], i, blocks[i]))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    ppm = open("mp-6-2.ppm", 'w+')
    print('P3\n%d %d\n255\n' % (image_width, image_height), file=ppm)
    count = 0
    for i in range(process_cnt):
        for item in blocks[i]:
            print(item, file=ppm,end=' ')
            count += 1
            if count % 3 == 0:
                print('\n', file=ppm, end='')
    ppm.close()

    print('Time elapsed:', int(time.time())-int(st))