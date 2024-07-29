from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile, User


# 下面这个代码段的作用是当 User 模型实例保存时（例如创建或更新用户），自动创建或更新与之关联的 UserProfile 模型实例
# 每当 User 模型实例保存后（无论是创建还是更新），都会触发 post_save 信号，执行标记的接收器函数 post_save_create_profile_receiver。
# User model 是sender，这个函数是receiver，要让sender和receiver连接起来
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('user profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
            print('Profile was not existed, but I create one')
        print('user is updated')