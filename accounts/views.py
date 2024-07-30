from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages, auth

from accounts.utils import detectUser
from vendor.forms import VendorForm


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
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
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            # vendor_name = v_form.cleaned_data['vendor_name']
            # vendor.vendor_slug = slugify(vendor_name) + '-' + str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('registerVendor')
        else:
            print("invalid form")
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form
    }
    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
