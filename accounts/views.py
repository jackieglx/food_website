from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.forms import UserForm
from accounts.models import User
from django.contrib import messages


# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # 方法1：使用form给密码加密
            # 首先从表单的清理数据中获取明文密码，然后通过 form.save(commit=False) 手动创建 User 对象，
            # 接着使用 set_password 方法加密密码，最后保存用户对象到数据库。
            # password = form.cleaned_data['password']
            # 下面是创建一个 User 对象，但不立即保存到数据库。这样可以在保存之前对对象进行进一步的修改，比如设置 role 属性。
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # 方法2：使用create_user给密码加密（核心区别是怎么创建user对象）
            # 从表单的清理数据中获取用户的各个字段，然后调用 User.objects.create_user 方法创建用户对象，
            # 并直接将对象保存到数据库中。
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.CUSTOMER
            user.save()
            print("User is created")
            messages.success(request, 'Your account has been registered successfully!')

            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)

    else:
        form = UserForm()

    form = UserForm()
    # context 的作用是将数据从视图函数传递到模板文件。
    # context 是一个字典，字典中的键是模板中可以访问的数据名称，值是实际的数据或对象。
    # 这里的 form 是一个表单对象，它将被传递到 registerUser.html 模板中，以便在页面上渲染和显示。
    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)
