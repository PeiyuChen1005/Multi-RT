from collections import namedtuple
import math
from ray import Ray
from vec3 import Vec3
hit_record = namedtuple('hit_record', ['p', 'normal', 't', 'material', 'front_face'])

def set_face_normal(r: Ray,outward_normal: Vec3):
    front_face = outward_normal.dot(r.direction) < 0
    return front_face

class Hitable:
    def hit(self, r: Ray, t_min, t_max, h_rec : hit_record):
        raise NotImplementedError('ERROR:NOT IMPLEMENTED!')

class Sphere(Hitable):
    def __init__(self, center, radius, material=None):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r: Ray, t_min, t_max):
        oc = r.origin-self.center
        a = r.direction.squared_length()
        b = 2* r.direction.dot(oc)
        c = oc.squared_length()-self.radius*self.radius
        delta = b*b - 4*a*c

        if delta > 0:
            temp = (-b-math.sqrt(delta))/(2*a)
            if t_min < temp <t_max:
                t = temp
                p = r.__call__(t)
                outward_normal = (p-self.center) /self.radius
                ff = set_face_normal(r, outward_normal)
                if ff:
                    normal = outward_normal
                else:
                    normal = -outward_normal

                return hit_record(p, normal, t, self.material, ff)

            temp = (-b + math.sqrt(delta)) / (2 * a)
            if t_min < temp < t_max:
                t = temp
                p = r.__call__(t)
                outward_normal = (p - self.center) / self.radius
                ff = set_face_normal(r, outward_normal)
                if ff:
                    normal = outward_normal
                else:
                    normal = -outward_normal

                return hit_record(p, normal, t, self.material, ff)

        return None

class HitableList(list, Hitable):
    def hit(self, r: Ray, t_min, t_max):
        hit_anything = False
        closest_so_far = t_max

        for obj in self:
            hit_rec = obj.hit(r, t_min, closest_so_far)
            if hit_rec:
                hit_anything = True
                closest_so_far = hit_rec.t
                result_rec = hit_rec

        if hit_anything:
            return result_rec



