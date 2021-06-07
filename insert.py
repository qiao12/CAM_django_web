import os
import random

if __name__ =='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CAM.settings")
    import django
    django.setup()
    from sales import models
    import random
    source_type = (('qq', "qq群"),
                   ('referral', "内部转介绍"),
                   ('website', "官方网站"),
                   ('baidu_ads', "百度推广"),
                   ('office_direct', "直接上门"),
                   ('WoM', "口碑"),
                   ('public_class', "公开课"),
                   ('website_luffy', "路飞官网"),
                   ('others', "其它"),)
    course_choices = (('LinuxL', 'Linux中高级'),
                      ('PythonFullStack', 'Python高级全栈开发'),)
    obj_list =[]
    for i in range(251):
        d = {
            'qq':'111111'+str(i),
            'name':'xiaopangpang'+str(i),
            'source':source_type[random.randint(0,8)][0],
            'course':course_choices[random.randint(0,1)][0],
        }
        obj = models.Customer(**d)
        obj_list.append(obj)
    models.Customer.objects.bulk_create(obj_list)