from collections import namedtuple
from vec3 import Vec3
from ray import Ray
import random
import math


def random_unit_vector():
    a = random.uniform(0, 2 * math.pi)
    b = random.uniform(-1, 1)
    r = math.sqrt(1 - b * b)
    return Vec3(r * math.cos(a), r * math.sin(a), b)


def random_in_unit_sphere():
    one = Vec3(1, 1, 1)

    while True:
        s = 2 * Vec3(random.random(), random.random(), random.random()) - one
        if s.squared_length() < 1:
            return s


scatter_rec = namedtuple('scattered_rec', ['scattered', 'attenuation'])


# 定义此结构体的原因是：在main_func中调用color_ray函数时需要用到此结构体中的两个变量，在后续代码中直接返回这个结构体信息可以方便的调用

class Material:
    def scatter(self, r_in: Ray, rec):
        raise NotImplementedError('ERROR:NOT IMPLEMENTED!')


class Lambertian(Material):
    def __init__(self, albedo):
        super().__init__()
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec):
        scatter_direction = rec.normal + random_unit_vector()
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo

        return scatter_rec(scattered, attenuation)


def reflect(v: Vec3, n: Vec3):
    return v - 2 * v.dot(n) * n


class Metal(Material):
    def __init__(self, albedo, fuzz=0):
        super().__init__()
        self.albedo = albedo
        self.fuzz = min(1, max(0, fuzz))

    def scatter(self, r_in: Ray, rec):
        reflect_direction = reflect(r_in.direction.unit_vector(), rec.normal)
        scattered = Ray(rec.p, reflect_direction + self.fuzz * random_unit_vector())
        attenuation = self.albedo
        if scattered.direction.dot(rec.normal) > 0:
            return scatter_rec(scattered, attenuation)
        return None


def refract(uv: Vec3, n: Vec3, etai_over_etat):
    cos_theta = -uv.dot(n)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(math.fabs(1.0 - r_out_perp.squared_length())) * n
    return r_out_perp + r_out_parallel


def schlick(cosine, ref_idx):
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1-r0) * (1-cosine)**5


class Dielectric(Material):
    def __init__(self, ref_idx):
        self.ref_idx = ref_idx

    def scatter(self, r_in: Ray, rec):
        attenuation = Vec3(1.0, 1.0, 1.0)
        if rec.front_face:
            etai_over_etat = 1.0 / self.ref_idx
        else:
            etai_over_etat = self.ref_idx
        unit_direction = r_in.direction.unit_vector()

        cos_theta = min(-unit_direction.dot(rec.normal), 1.0)
        sin_theta = math.sqrt(1.0-cos_theta * cos_theta)
        if etai_over_etat * sin_theta > 1.0:
            reflected = reflect(unit_direction, rec.normal)
            scattered = Ray(rec.p, reflected)
            return scatter_rec(scattered, attenuation)

        reflect_prob = schlick(cos_theta, etai_over_etat)
        if random.random() < reflect_prob:
            reflected = reflect(unit_direction, rec.normal)
            scattered = Ray(rec.p, reflected)
            return scatter_rec(scattered, attenuation)

        refracted = refract(unit_direction, rec.normal, etai_over_etat)
        scattered = Ray(rec.p, refracted)
        return scatter_rec(scattered, attenuation)
