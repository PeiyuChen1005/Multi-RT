from vec3 import Vec3
from ray import Ray
from hitable import Hitable,HitableList,Sphere
import sys
from camera import Camera
from queue import Queue
import threading as td
import multiprocessing as mp
import random
import time
# image
aspect_ratio = 16.0 / 9.0  # height/width
image_width = 320
image_height = int(image_width / aspect_ratio)
sample_per_pixel =100
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
        return 0.5*(hit_rec.normal + Vec3(1,1,1))
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
    with mp.Manager() as MG:
        # color block
        block_0 = mp.Manager().list([])
        block_1 = mp.Manager().list([])
        block_2 = mp.Manager().list([])
        block_3 = mp.Manager().list([])

    st = time.time()
    #coordinates
    coordinates = [[0, image_height, image_width, int(3*image_height/4)],
                   [0, int(3*image_height/4), image_width, int(1*image_height/2)],
                   [0, int(1*image_height/2), image_width, int(1*image_height/4)],
                   [0, int(1*image_height/4), image_width, 0]]

    #result
    processes = []


    p0 = mp.Process(target=color_block, args=(coordinates[0], 0, block_0))
    p0.start()
    processes.append(p0)

    p1 = mp.Process(target=color_block, args=(coordinates[1], 1, block_1))
    p1.start()
    processes.append(p1)

    p2 = mp.Process(target=color_block, args=(coordinates[2], 2, block_2))
    p2.start()
    processes.append(p2)

    p3 = mp.Process(target=color_block, args=(coordinates[3], 3, block_3))
    p3.start()
    processes.append(p3)

    for process in processes:
        process.join()

    ppm = open("mp-6-1.ppm", 'w+')
    print('P3\n%d %d\n255\n' % (image_width, image_height), file=ppm)
    count = 0
    for i in block_0:
        print(i,file=ppm,end=' ')
        count += 1
        if count % 3 == 0:
            print('\n',file=ppm,end='')
    for i in block_1:
        print(i,file=ppm,end=' ')
        count += 1
        if count % 3 == 0:
            print('\n',file=ppm,end='')
    for i in block_2:
        print(i,file=ppm,end=' ')
        count += 1
        if count % 3 == 0:
            print('\n',file=ppm,end='')
    for i in block_3:
        print(i,file=ppm,end=' ')
        count += 1
        if count % 3 == 0:
            print('\n',file=ppm,end='')

    ppm.close()

    print('Time elapsed:', int(time.time())-int(st))