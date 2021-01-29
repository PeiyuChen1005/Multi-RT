from ray import Ray
from vec3 import Vec3
import math
import random


def random_in_unit_disk():
    while True:
        p = Vec3(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), 0)
        if p.squared_length() < 1:
            return p


class Camera:
    def __init__(self, ori: Vec3, hor: Vec3, ver: Vec3, llc: Vec3):
        self.origin = ori
        self.lower_left_corner = llc
        self.horizontal = hor
        self.vertical = ver

    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)


class FOVCamera:
    def __init__(self, vfov, aspect_ratio):
        theta = math.radians(vfov)
        h = math.tan(theta / 2)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height
        focal_length = 1.0

        origin = Vec3(0.0, 0.0, 0.0)
        horizontal = Vec3(viewport_width, 0.0, 0.0)
        vertical = Vec3(0.0, viewport_height, 0.0)
        lower_left_corner = origin - horizontal / 2 - vertical / 2 - Vec3(0, 0, focal_length)

        self.origin = origin
        self.horizontal = horizontal
        self.vertical = vertical
        self.lower_left_corner = lower_left_corner

    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)

class PositionalCamera:
    def __init__(self, lookfrom: Vec3, lookat: Vec3, vup: Vec3, vfov, aspect_ratio, aperture, dist_to_focus):
        theta = math.radians(vfov)
        h = math.tan(theta / 2)     #默认focal_length = 1
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        w = (lookfrom-lookat).unit_vector()
        u = (vup.cross(w)).unit_vector()
        v = w.cross(u)

        origin = lookfrom
        horizontal = dist_to_focus * viewport_width * u
        vertical = dist_to_focus * viewport_height * v
        lower_left_corner = origin - horizontal / 2 - vertical / 2 - dist_to_focus * w

        self.origin = origin
        self.horizontal = horizontal
        self.vertical = vertical
        self.lower_left_corner = lower_left_corner
        self.lens_radius = aperture / 2

        self.u = u
        self.v = v
    def get_ray(self,s,t):
        lens_disk = self.lens_radius * random_in_unit_disk()
        offset = lens_disk.x * self.u + lens_disk.y * self.v
        return Ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)


