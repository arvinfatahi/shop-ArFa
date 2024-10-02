from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from .decorators import check_position
from azbankgateways.models import Bank
import jdatetime
from datetime import datetime

from myShop.models import (
    UserModel,
    ProductModel,
    CategoryModel,
    TicketModel,
    ReplayTicketModel,
    BrandModel,
    GalleryProductModel,
    AdvertisingModel,
    DiscountCodeModel,
    FactorModel,
    FactorProductModel,
    AboutModel,
    )
from .forms import (
    EditInfoForm,

    EditUsernameForm,
    EditPasswordForm,

    EditEmployeeAdminForm,
    AddEmployeeForm,
    EditEmployeeForm,

    AddCategoryForm,
    EditCategoryForm,

    AddBrandForm,
    EditBrandForm,

    AddImagesProductForm,
    AddProductForm,
    EditProductForm,

    EditUserForm,

    SendTicketAdminForm,
    ReplyTicketForm,

    AdvertisingForm,
    EditAdvertisingForm,

    DiscountCodeForm,
    EditDiscountCodeForm,

    AddAboutForm,
    EditAboutForm,

    EditProductPrice,

    setEmployeeRightForm,
    )

# Create your views here.

def admin_only(user):
    return user.position == 1

def support_only(user):
    return user.position == 2

def product_registration_only(user):
    return user.position == 3

def finance_only(user):
    return user.position == 4

def product_post_only(user):
    return user.position == 5
# ========================================= start panel admin

@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def adminPanel(request):
    employee_count = UserModel.objects.filter(is_staff=True, is_superuser=False).count()
    product_count = ProductModel.objects.all()
    user_count = UserModel.objects.filter(Q(is_superuser=False) & Q(is_staff=False)).count()
    category_count = CategoryModel.objects.all()
    brand_count = BrandModel.objects.all()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/admin_panel.html', {
        'employee_count':employee_count,
        'product_count':product_count,
        'user_count':user_count,
        'category_count':category_count,
        'brand_count':brand_count,
        'ticket_admin':ticket_admin
    })

@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def infoAdmin(request):
    edit_info_form = EditInfoForm()
    edit_username_users_form = EditUsernameForm()
    edit_password_users_form = EditPasswordForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/info_admin.html', {
        'edit_info_form':edit_info_form,
        'edit_username_users_form':edit_username_users_form,
        'edit_password_users_form':edit_password_users_form,
        'ticket_admin':ticket_admin
    })

def editAdmin(request, id_admin):
    if request.method == 'POST':
        edit_form_full = EditInfoForm(request.POST, request.FILES)
        if edit_form_full.is_valid():
            admin_find = UserModel.objects.filter(id=id_admin).first()
            admin_find.first_name = edit_form_full.cleaned_data['first_name']
            admin_find.last_name = edit_form_full.cleaned_data['last_name']
            admin_find.email = edit_form_full.cleaned_data['email']
            admin_find.phone = edit_form_full.cleaned_data['phone']
            admin_find.address = edit_form_full.cleaned_data['address']
            if 'image' in request.FILES:
                admin_find.image = request.FILES['image']
            admin_find.save()
            messages.success(request, 'ویرایش با موفقیت انجام شد.')
            return redirect('infoAdmin')
        else:
            messages.success(request, edit_form_full.errors)
            return redirect('infoAdmin')
    else:
        return redirect('infoAdmin')

def editPasswordAdmin(request, id_admin):
    if request.method == 'POST':
        change_password_form_full = EditPasswordForm(request.POST)
        if change_password_form_full.is_valid():
            password1 = change_password_form_full.cleaned_data['password1']
            password2 = change_password_form_full.cleaned_data['password2']
            if password1 == password2:
                find_admin_password = UserModel.objects.filter(id=id_admin).first()
                find_admin_password.set_password(password1)
                find_admin_password.save()
                login(request, find_admin_password)
                messages.success(request, 'رمز عبور مدیر با موفقیت ویرایش شد.')
                return redirect('infoAdmin')
            else:
                messages.success(request, 'رمز عبور با هم تطابق ندارند.')
                return redirect('infoAdmin')
        else:
            messages.error(request, change_password_form_full.errors)
            return redirect('infoAdmin')
    else:
        return redirect('infoAdmin')

def editUsernameAdmin(request, id_admin):
    if request.method == 'POST':
        edit_username_form_full = EditUsernameForm(request.POST)
        if edit_username_form_full.is_valid():
            find_admin_user = UserModel.objects.filter(id=id_admin).first()
            find_admin_user.username = edit_username_form_full.cleaned_data['username']
            find_admin_user.save()
            messages.success(request, 'نام کاربری مدیر با موفقیت ویرایش شد.')
            return redirect('infoAdmin')
        else:
            messages.success(request, edit_username_form_full.errors)
            return redirect('infoAdmin')
    else:
        return redirect('infoAdmin')

def loginAdmin(request):
    if request.method == 'POST':
        authentication_form = AuthenticationForm(data=request.POST)
        if authentication_form.is_valid():
            username = authentication_form.cleaned_data['username']
            password = authentication_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:  # بررسی کاربر معتبر
                if user.is_staff and not user.is_superuser:
                    employee = UserModel.objects.get(id=user.id)
                    if employee.position == 2:
                        login(request, user)
                        return redirect('eSupport')
                    elif employee.position == 3:
                        login(request, user)
                        return redirect('eProductRegistration')
                    elif employee.position == 4:
                        login(request, user)
                        return redirect('eFinance')
                    elif employee.position == 5:
                        login(request, user)
                        return redirect('eProductPost')
                elif user.is_superuser:
                    login(request, user)
                    return redirect('adminPanel')
            else:
                messages.error(request, 'کارمندی با این مشخصات وجود ندارد.')
                return redirect('login')
        else:
            messages.error(request, authentication_form.errors)
            return redirect('login')
    else:
        authentication_form = AuthenticationForm()
        return render(request, 'registration/login.html', {
            'authentication_form': authentication_form
        })


def logoutAdmin(request):
    logout(request)
    return redirect('login')

# ========================================= end panel admin
# ========================================= start products
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aProducts(request):
    products = ProductModel.objects.all()
    add_images_product_form = AddImagesProductForm()
    add_product_form = AddProductForm()
    gallery_product_model = GalleryProductModel.objects.all()
    edit_product_form = EditProductForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()
    
    return render(request, 'registration/admin/a_products.html', {
        'products':products,
        'add_images_product_form':add_images_product_form,
        'add_product_form':add_product_form,
        'gallery_product_model':gallery_product_model,
        'edit_product_form':edit_product_form,
        'ticket_admin':ticket_admin
    })

def aAddProduct(request):
    if request.method == 'POST':
        add_product_form_full = AddProductForm(request.POST, request.FILES)
        if add_product_form_full.is_valid():
            name_product = add_product_form_full.cleaned_data['name']
            price_product = add_product_form_full.cleaned_data['price']
            category_product = add_product_form_full.cleaned_data['category']
            description_product = add_product_form_full.cleaned_data['description']
            image_product = request.FILES['image']
            is_sale_product = add_product_form_full.cleaned_data['is_sale']
            sale_price_product = add_product_form_full.cleaned_data['sale_price']
            number_product = add_product_form_full.cleaned_data['number']
            slider_product = add_product_form_full.cleaned_data['slider']
            state_product = add_product_form_full.cleaned_data['state']
            new_product = ProductModel(name=name_product, price=price_product, category=category_product, description=description_product, is_sale=is_sale_product, sale_price=sale_price_product, image=image_product, number=number_product, slider=slider_product, state=state_product)
            new_product.save()
            messages.success(request, 'این محصول با موفقیت ثبت شد')
            return redirect('aProducts')
        else:
            messages.success(request, add_product_form_full.errors)
            return redirect('aProducts')
    else:
        return redirect('aProducts')

def aAddImagesProduct(request, id_product):
    if request.method == 'POST':
        if GalleryProductModel.objects.count() >= 4:
            messages.success(request, 'شما فقط می توانید 4 تصویر برای هر محصول اضافه کنید.')
            return redirect('aProducts')
        else:
            add_images_product_form_full = AddImagesProductForm(request.POST, request.FILES)
            if add_images_product_form_full.is_valid():
                image = add_images_product_form_full.cleaned_data['image']
                images_product = GalleryProductModel(image=image, product_id=id_product)
                images_product.save()
                messages.success(request, 'تصویر با موفقیت با گالری اضافه شد.')
                return redirect('aProducts')
            else:
                messages.error(request, add_images_product_form_full.errors)
                return redirect('aProducts')
    else:
        return redirect('aProducts')

def aDeleteImages(request, id_image):
    image_find = GalleryProductModel.objects.filter(id=id_image).first()
    image_find.delete()
    messages.success(request, 'تصویر با موفقیت حذف شد.')

    return redirect('aProducts')

def aEditProduct(request, id_product):
    if request.method == 'POST':
        edit_product_form_full = EditProductForm(request.POST, request.FILES)
        if edit_product_form_full.is_valid():
            edit_product_find = ProductModel.objects.filter(id=id_product).first()
            edit_product_find.name = edit_product_form_full.cleaned_data['name']
            edit_product_find.price = edit_product_form_full.cleaned_data['price']
            edit_product_find.category = edit_product_form_full.cleaned_data['category']
            edit_product_find.description = edit_product_form_full.cleaned_data['description']
            if 'image' in request.FILES:
                edit_product_find.image = request.FILES['image']
            edit_product_find.is_sale = edit_product_form_full.cleaned_data['is_sale']
            edit_product_find.sale_price = edit_product_form_full.cleaned_data['sale_price']
            edit_product_find.number = edit_product_form_full.cleaned_data['number']
            edit_product_find.slider = edit_product_form_full.cleaned_data['slider']
            edit_product_find.state = edit_product_form_full.cleaned_data['state']
            edit_product_find.save()
            messages.success(request, 'این محصول با موفقیت ویرایش شد.')
            return redirect('aProducts')
        else:
            messages.success(request, edit_product_form_full.errors)
            return redirect('aProducts')
    else:
        return redirect('aProducts')

def aDeleteProduct(request, id_product):
    delete_product = ProductModel.objects.filter(id=id_product).first()
    delete_product.delete()
    messages.success(request, 'حدف محصول با موفقیت انجام شد.')
    return redirect('aProducts')

# ========================================= end products
# ========================================= start employee
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aEmployee(request):
    employees = UserModel.objects.filter(is_staff=True, is_superuser=False)
    for employee in employees:
        employee.shamsi_date_joined = jdatetime.datetime.fromgregorian(datetime=employee.date_joined).strftime('%Y/%m/%d')
    add_employee_form = AddEmployeeForm()
    edit_employee_form = EditEmployeeForm()
    edit_username_form = EditUsernameForm()
    edit_password_form = EditPasswordForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_employee.html', {
        'employees':employees,
        'add_employee_form':add_employee_form,
        'edit_employee_form':edit_employee_form,
        'edit_username_form':edit_username_form,
        'edit_password_form':edit_password_form,
        'ticket_admin':ticket_admin
    })

def aAddEmployee(request):
    if request.method == 'POST':
        add_employee_form_full = AddEmployeeForm(request.POST, request.FILES)
        if add_employee_form_full.is_valid():
            add_employee_form_full.save()
            messages.success(request, 'کارمند با موفقیت ثبت شد.')
            return redirect('aEmployee')
        else:
            messages.success(request, add_employee_form_full.errors)
            return redirect('aEmployee')
    else:
        return redirect('aEmployee')

def aEditEmployee(request, id_employee):
    if request.method == 'POST':
        employee_form_full = EditEmployeeForm(request.POST, request.FILES)
        if employee_form_full.is_valid():
            edit_employee_find = UserModel.objects.filter(id=id_employee).first()
            edit_employee_find.first_name = employee_form_full.cleaned_data['first_name']
            edit_employee_find.last_name = employee_form_full.cleaned_data['last_name']
            edit_employee_find.position = employee_form_full.cleaned_data['position']
            edit_employee_find.email = employee_form_full.cleaned_data['email']
            edit_employee_find.phone = employee_form_full.cleaned_data['phone']
            edit_employee_find.address = employee_form_full.cleaned_data['address']
            edit_employee_find.right = employee_form_full.cleaned_data['right']
            if 'image' in request.FILES:
                edit_employee_find.image = request.FILES['image']
            edit_employee_find.save()
            messages.success(request, 'ویرایش کارمند با موفقیت انجام شد.')
            return redirect('aEmployee')
        else:
            messages.success(request, employee_form_full.errors)
            return redirect('aEmployee')
    else:
        return redirect('aEmployee')

def aDeleteEmployee(request, id_employee):
    delete_employee = UserModel.objects.filter(id=id_employee).first()
    delete_employee.delete()
    messages.success(request, 'حدف کارمند با موفقیت انجام شد.')
    return redirect('aEmployee')

@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aSettingEmployee(request, id_employee):
    employee = UserModel.objects.filter(id=id_employee).first()
    change_username_employee_form = EditUsernameForm(instance=employee)
    change_pass_employee_form = EditPasswordForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_setting_employee.html', {
        'employee':employee,
        'change_username_employee_form':change_username_employee_form,
        'change_pass_employee_form':change_pass_employee_form,
        'ticket_admin':ticket_admin
    })

def changePassAdminEmployee(request, id_employee):
    if request.method == 'POST':
        change_password_admin_employee_form_full = EditPasswordForm(request.POST)
        if change_password_admin_employee_form_full.is_valid():
            password1 = change_password_admin_employee_form_full.cleaned_data['password1']
            password2 = change_password_admin_employee_form_full.cleaned_data['password2']
            if password1 == password2:
                find_employee_password = UserModel.objects.filter(id=id_employee).first()
                find_employee_password.set_password(password1)
                find_employee_password.save()
                messages.success(request, 'رمز عبور کارمند با موفقیت ویرایش شد.')
                return redirect('aEmployee')
            else:
                messages.success(request, 'رمز عبور با هم تطابق ندارند.')
                return redirect('aEmployee')
        else:
            messages.success(request, change_password_admin_employee_form_full.errors)
            return redirect('aEmployee')
    else:
        return redirect('aEmployee')

def changeUsernameAdminEmployee(request, id_employee):
    if request.method == 'POST':
        change_username_admin_employee_form_full = EditUsernameForm(request.POST)
        if change_username_admin_employee_form_full.is_valid():
            find_admin_user = UserModel.objects.filter(id=id_employee).first()
            find_admin_user.username = change_username_admin_employee_form_full.cleaned_data['username']
            find_admin_user.save()
            messages.success(request, 'نام کاربری کارمند با موفقیت ویرایش شد.')
            return redirect('aEmployee')
        else:
            messages.success(request, change_username_admin_employee_form_full.errors)
            return redirect('aEmployee')
    else:
        return redirect('aEmployee')

# ========================================= end employee
# ========================================= start users
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aUsers(request):
    edit_users_form = EditUserForm()
    edit_username_users_form = EditUsernameForm()
    edit_password_users_form = EditPasswordForm()
    users = UserModel.objects.filter(Q(is_superuser=False) & Q(is_staff=False)).all()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_users.html', {
        'edit_users_form':edit_users_form,
        'edit_username_users_form':edit_username_users_form,
        'edit_password_users_form':edit_password_users_form,
        'users':users,
        'ticket_admin':ticket_admin
    })

def aEditUsers(request, id_user):
    if request.method == 'POST':
        edit_user_form_full = EditUserForm(request.POST)
        if edit_user_form_full.is_valid():
            edit_user_find = UserModel.objects.filter(id=id_user).first()
            edit_user_find.first_name = edit_user_form_full.cleaned_data['first_name']
            edit_user_find.last_name = edit_user_form_full.cleaned_data['last_name']
            edit_user_find.email = edit_user_form_full.cleaned_data['email']
            edit_user_find.phone = edit_user_form_full.cleaned_data['phone']
            edit_user_find.address = edit_user_form_full.cleaned_data['address']
            edit_user_find.save()
            messages.success(request, 'کاربر با موفقیت ویرایش شد.')
            return redirect('aUsers')
        else:
            messages.success(request, edit_user_form_full.errors)
            return redirect('aUsers')
    else:
        return redirect('aUsers')

def aDeleteUser(request, id_user):
    delete_user = UserModel.objects.filter(id=id_user).first()
    delete_user.delete()
    messages.success(request, 'حدف کاربر با موفقیت انجام شد.')
    return redirect('aUsers')

def changePassAdminUser(request, id_user):
    if request.method == 'POST':
        change_pass_user_form = EditPasswordForm(request.POST)
        if change_pass_user_form.is_valid():
            password1 = change_pass_user_form.cleaned_data['password1']
            password2 = change_pass_user_form.cleaned_data['password2']
            if password1 == password2:
                user_find = UserModel.objects.filter(id=id_user).first()
                user_find.set_password(password1)
                user_find.save()
                messages.success(request, 'رمز عبور کاربر با موفقیت ویرایش شد.')
                return redirect('aUsers')
            else:
                messages.error(request, 'رمز عبور با هم تطابق ندارد.')
                return redirect('aUsers')
        else:
            return redirect('aUsers')
    else:
        return redirect('aUsers')

def changeUsernameAdminUser(request, id_user):
    if request.method == 'POST':
        edit_username_user_form = EditUsernameForm(request.POST)
        if edit_username_user_form.is_valid():
            user_find = UserModel.objects.filter(id=id_user).first()
            user_find.username = edit_username_user_form.cleaned_data['username']
            user_find.save()
            messages.success(request, 'نام کاربری با موفقیت ویرایش شد.')
            return redirect('aUsers')
        else:
            messages.error(request, edit_username_user_form.errors)
            return redirect('aUsers')
    else:
        return redirect('aUsers')

# ========================================= end users
# ========================================= start category
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aCategory(request):
    categorys = CategoryModel.objects.all()
    add_category_form = AddCategoryForm()
    edit_category_form = EditCategoryForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_category.html', {
        'categorys':categorys,
        'add_category_form':add_category_form,
        'edit_category_form':edit_category_form,
        'ticket_admin':ticket_admin
    })

def aAddCategory(request):
    if request.method == 'POST':
        add_category_form_full = AddCategoryForm(data=request.POST)
        if add_category_form_full.is_valid():
            category_name = add_category_form_full.cleaned_data['category_name']
            new_category = CategoryModel(name=category_name)
            new_category.save()
            messages.success(request, 'دسته مورد نظر با موفقیت اضافه شد.')
            return redirect('aCategory')
        else:
            messages.success(request, add_category_form_full.errors)
            return redirect('aCategory')
    else:
        return redirect('aCategory')

def aEditCategory(request, id_category):
    if request.method == 'POST':
        name_category = EditCategoryForm(request.POST)
        if name_category.is_valid():
            find_category = CategoryModel.objects.filter(id=id_category).first()
            find_category.name = name_category.cleaned_data['name']
            find_category.save()
            messages.success(request, 'ویرایش دسته با موفقیت انجام شد.')
            return redirect('aCategory')
        else:
            messages.success(request, name_category.errors)
            return redirect('aCategory')
    else:
        return redirect('aCategory')

def aDeleteCategory(request, id_category):
    delete_category = CategoryModel.objects.filter(id=id_category).first()
    delete_category.delete()
    messages.success(request, 'حدف دسته با موفقیت انجام شد.')
    return redirect('aCategory')

# ========================================= end category
# ========================================= start brand
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aBrand(request):
    brand_show = BrandModel.objects.all()
    add_brand_form = AddBrandForm()
    edit_brand_form = EditBrandForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_brand.html', {
        'brand_show':brand_show,
        'add_brand_form':add_brand_form,
        'edit_brand_form':edit_brand_form,
        'ticket_admin':ticket_admin
    })

def aAddBrand(request):
    if request.method == 'POST':
        brand_form_full = AddBrandForm(request.POST, request.FILES)
        if brand_form_full.is_valid():
            name = brand_form_full.cleaned_data['name']
            image = request.FILES['image']
            brand_add = BrandModel(name=name, image=image)
            brand_add.save()
            messages.success(request, 'برند با موفقیت اضافه شد.')
            return redirect('aBrand')
        else:
            messages.error(request, brand_form_full.errors)
            return redirect('aBrand')
    else:
        return redirect('aBrand')

def aEditBrand(request, id_brand):
    if request.method == 'POST':
        edit_brand_form_full = EditBrandForm(request.POST, request.FILES)
        if edit_brand_form_full.is_valid():
            brand_find = BrandModel.objects.filter(id=id_brand).first()
            brand_find.name = edit_brand_form_full.cleaned_data['name']
            if 'image' in request.FILES:
                brand_find.image = request.FILES['image']
            brand_find.save()
            messages.success(request, 'برند با موفقیت ویرایش شد.')
            return redirect('aBrand')
        else:
            messages.error(request, edit_brand_form_full.errors)
            return redirect('aBrand')
    else:
        return redirect('aBrand')

def aDeleteBrand(request, id_brand):
    brand_delete = BrandModel.objects.filter(id=id_brand).first()
    brand_delete.delete()
    messages.success(request, 'برند با موفقیت حذف شد.')
    return redirect('aBrand')

# ========================================= end brand
# ========================================= start ticket admin
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def ticketAdmin(request, id_admin):
    ticket_receive_admin = TicketModel.objects.filter(receive_id=id_admin).all()
    ticket_send_admin = TicketModel.objects.filter(send_id=id_admin).all()
    users = UserModel.objects.all()
    reply_ticket_form = ReplyTicketForm()
    send_ticket_admin_form = SendTicketAdminForm()
    ticket_admin = TicketModel.objects.filter(receive_id=id_admin, state=1).all()

    return render(request, 'registration/admin/ticket_admin.html', {
        'ticket_receive_admin':ticket_receive_admin,
        'ticket_send_admin':ticket_send_admin,
        'users':users,
        'reply_ticket_form':reply_ticket_form,
        'send_ticket_admin_form':send_ticket_admin_form,
        'ticket_admin':ticket_admin
    })

@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def showTicketAdmin(request, id_ticket):
    all_categorys = CategoryModel.objects.all()
    users = UserModel.objects.all()
    ticket_show = TicketModel.objects.filter(id=id_ticket).first()
    show_replay_ticket = ReplayTicketModel.objects.filter(ticket_id=id_ticket).all()
    
    if ticket_show:
        ticket_show.shamsi_date_ticket = jdatetime.datetime.fromgregorian(datetime=ticket_show.created).strftime('%Y/%m/%d')
    
    for replay in show_replay_ticket:
        replay.shamsi_date_replay_ticket = jdatetime.datetime.fromgregorian(datetime=replay.created).strftime('%Y/%m/%d')

    replay_ticket_form = ReplyTicketForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_show_ticket.html', {
        'all_categorys': all_categorys,
        'users': users,
        'ticket_show': ticket_show,
        'replay_ticket_form': replay_ticket_form,
        'show_replay_ticket': show_replay_ticket,
        'ticket_admin': ticket_admin
    })


def deleteTicketAdmin(request, id_ticket):
    ticket_find = TicketModel.objects.filter(id=id_ticket).first()
    ticket_find.delete()
    messages.success(request, 'تیکت با موفقیت حذف شد.')
    return redirect('ticketAdmin', request.user.id)

def replayTicketAdmin(request, id_admin, id_ticket):
    if request.method == 'POST':
        text = request.POST.get('text')
        ticket_find = TicketModel.objects.filter(id=id_ticket).first()
        if ticket_find:
            ticket_find.state = 0
            ticket_find.save()
            sender = UserModel.objects.get(id=id_admin)
            ticket_add = ReplayTicketModel(replay_text=text, ticket=ticket_find, sender=sender)
            ticket_add.save()
            messages.success(request, 'پاسخ تیکت با موفقیت ارسال شد.')
            return redirect('showTicketAdmin', id_ticket)
        else:
            messages.error(request, 'تیکت مورد نظر یافت نشد..')
            return redirect('showTicketAdmin', id_ticket)
    else:
        return redirect('showTicketAdmin', id_ticket)

# ===================================================================== end ticket admin
# ===================================================================== start advertising
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aMainAvertising(request):
    advertising_form = AdvertisingForm()
    advertisings_show = AdvertisingModel.objects.all()
    edit_advertising_form = EditAdvertisingForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_main_advertising.html', {
        'advertising_form':advertising_form,
        'advertisings_show':advertisings_show,
        'edit_advertising_form':edit_advertising_form,
        'ticket_admin':ticket_admin
    })

def aAddMainAdvertising(request):
    if request.method == 'POST':
        if AdvertisingModel.objects.count() >= 4:
            messages.success(request, 'شما فقط می توانید 4 تصویر تبلیغاتی اضافه کنید.')
            return redirect('aMainAvertising')
        else:
            add_advertising_form_full = AdvertisingForm(request.POST, request.FILES)
            if add_advertising_form_full.is_valid():
                text_advertising = add_advertising_form_full.cleaned_data['text']
                image_advertising = request.FILES['image']
                title_advertising = add_advertising_form_full.cleaned_data['title']
                description_advertising = add_advertising_form_full.cleaned_data['description']
                new_advertising = AdvertisingModel(text=text_advertising, image=image_advertising, title=title_advertising, description=description_advertising)
                new_advertising.save()
                messages.success(request, 'تبلیغات با موفقیت اضافه شد.')
                return redirect('aMainAvertising')
            else:
                messages.success(request, add_advertising_form_full.errors)
                return redirect('aMainAvertising')
    else:
        return redirect('aMainAvertising')

def aEditMainAdvertising(request, id_advertising):
    if request.method == 'POST':
        edit_advertising_form = EditAdvertisingForm(request.POST, request.FILES)
        if edit_advertising_form.is_valid():
            advertising_find = AdvertisingModel.objects.filter(id=id_advertising).first()
            advertising_find.text = edit_advertising_form.cleaned_data['text']
            if 'image' in request.FILES:
                advertising_find.image = request.FILES['image']
            advertising_find.title = edit_advertising_form.cleaned_data['title']
            advertising_find.description = edit_advertising_form.cleaned_data['description']
            advertising_find.save()
            messages.success(request, 'ویرایش با موفقیت انجام شد.')
            return redirect('aMainAvertising')
        else:
            messages.success(request, edit_advertising_form.errors)
            return redirect('aMainAvertising')
    else:
        return render('aMainAvertising')

def aDeleteAdvertising(request, id_advertising):
    delete_advertising = AdvertisingModel.objects.filter(id=id_advertising).first()
    delete_advertising.delete()
    messages.success(request, 'حذف تبلیغ با موفقیت انجام شد.')
    return redirect('aMainAvertising')

# ===================================================================== end advertising
# ===================================================================== start discount code
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aDiscountCode(request):
    all_discount_code = DiscountCodeModel.objects.all()
    for discount_code in all_discount_code:
        discount_code.shamsi_start_date = jdatetime.datetime.fromgregorian(datetime=discount_code.start_date).strftime('%Y/%m/%d')
        discount_code.shamsi_end_date = jdatetime.datetime.fromgregorian(datetime=discount_code.end_date).strftime('%Y/%m/%d')

    discount_code_form = DiscountCodeForm()
    edit_discount_code_form = EditDiscountCodeForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()
    
    return render(request, 'registration/admin/a_discount_code.html', {
        'all_discount_code': all_discount_code,
        'discount_code_form': discount_code_form,
        'edit_discount_code_form': edit_discount_code_form,
        'ticket_admin': ticket_admin
    })

def aAddDiscountCode(request):
    if request.method == 'POST':
        discount_code_form_full = DiscountCodeForm(request.POST)
        if discount_code_form_full.is_valid():
            discount_code = discount_code_form_full.cleaned_data['discount_code']
            discount_percent = discount_code_form_full.cleaned_data['discount_percent']
            description = discount_code_form_full.cleaned_data['description']
            end_date_shamsi = discount_code_form_full.cleaned_data['end_date']  # تاریخ شمسی
            is_active = discount_code_form_full.cleaned_data['is_active']

            # تبدیل تاریخ شمسی به میلادی
            if end_date_shamsi:
                # end_date_shamsi به عنوان یک شیء date است، بنابراین مستقیماً از آن استفاده می‌کنیم
                end_date_miladi = end_date_shamsi.togregorian()  # تبدیل به میلادی
                end_date = datetime(end_date_miladi.year, end_date_miladi.month, end_date_miladi.day)  # تبدیل به datetime

            # ذخیره در مدل
            new_discount_code = DiscountCodeModel(
                discount_code=discount_code,
                discount_percent=discount_percent,
                description=description,
                end_date=end_date,  # تاریخ میلادی
                is_active=is_active
            )
            new_discount_code.save()
            messages.success(request, 'کد تخفیف اضافه شد.')
            return redirect('aDiscountCode')
        else:
            messages.error(request, discount_code_form_full.errors)
            return redirect('aDiscountCode')
    else:
        return redirect('aDiscountCode')

def aEditDiscountCode(request, id_discountCode):
    if request.method == 'POST':
        find_discount_code = DiscountCodeModel.objects.filter(id=id_discountCode).first()
        edit_discount_code_form = EditDiscountCodeForm(request.POST, instance=find_discount_code)
        if edit_discount_code_form.is_valid():
            edit_discount_code_form.save()
            messages.success(request, 'کد تخفیف با موفقیت ویرایش شد.')
            return redirect('aDiscountCode')
        else:
            messages.error(request, edit_discount_code_form.errors)
            return redirect('aDiscountCode')
    else:
        return redirect('aDiscountCode')

def aDeleteDiscountCode(request, id_discountCode):
    delete_discount_code = DiscountCodeModel.objects.filter(id=id_discountCode).first()
    delete_discount_code.delete()
    messages.success(request, 'حدف کد تخفیف با موفقیت انجام شد.')
    return redirect('aDiscountCode')

# ===================================================================== end discount code
# ===================================================================== start bank transactions
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aBankTransactions(request):
    transactions = Bank.objects.all()
    for transaction in transactions:
        transaction.shamsi_date = jdatetime.datetime.fromgregorian(datetime=transaction.created_at).strftime('%Y/%m/%d')
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()
    
    return render(request, 'registration/admin/a_bank_transactions.html', {
        'transactions':transactions,
        'ticket_admin':ticket_admin
    })

# ===================================================================== end bank transactions
# ===================================================================== start buy factors
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aBuyFactors(request):
    factor_show = FactorModel.objects.all()
    for factor in factor_show:
        factor.shamsi_date = jdatetime.datetime.fromgregorian(datetime=factor.buy_data).strftime('%Y/%m/%d')
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_buy_factors.html', {
        'factor_show':factor_show,
        'ticket_admin':ticket_admin
    })

@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def showProductsUser(request, id_factor):
    factor_product_show =  FactorProductModel.objects.filter(factor_id=id_factor).all()
    for product in factor_product_show:
        product.shamsi_buy_date = jdatetime.datetime.fromgregorian(datetime=product.factor.buy_data).strftime('%Y/%m/%d')
    
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_show_products_user.html', {
        'factor_product_show':factor_product_show,
        'ticket_admin':ticket_admin
    })

# ===================================================================== end buy factors
# ===================================================================== start about admin
@user_passes_test(admin_only, login_url='/accounts/login/')
@check_position([1])
def aAbout(request):
    add_about_form = AddAboutForm()
    about_show = AboutModel.objects.all()
    edit_about_form = EditAboutForm()
    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/admin/a_about.html', {
        'add_about_form':add_about_form,
        'about_show':about_show,
        'edit_about_form':edit_about_form,
        'ticket_admin':ticket_admin
    })

def aAddAboutMembers(request):
    if request.method == 'POST':
        add_about_form_full = AddAboutForm(request.POST, request.FILES)
        if add_about_form_full.is_valid():
            add_about_form_full.save()
            messages.success(request, 'اعضا با موفقیت اضافه شد.')
            return redirect('aAbout')
        else:
            messages.error(request, add_about_form_full.errors)
            return redirect('aAbout')
    else:
        return redirect('aAbout')

def aEditAboutMembers(request, id_about):
    if request.method == 'POST':
        edit_about_form = EditAboutForm(request.POST, request.FILES)
        if edit_about_form.is_valid():
            find_about = AboutModel.objects.filter(id=id_about).first()
            find_about.about = edit_about_form.cleaned_data['about']
            if 'image' in request.FILES:
                find_about.image = request.FILES['image']
            find_about.save()
            messages.error(request, 'ویرایش با موفقیت انجام شد.')
            return redirect('aAbout')
        else:
            messages.error(request, edit_about_form.errors)
            return redirect('aAbout')
    else:
        return redirect('aAbout')

def aDeleteAbout(request, id_about):
    abourt_find = AboutModel.objects.filter(id=id_about).first()
    abourt_find.delete()
    messages.success(request, 'فیلد با موفقیت حذف شد.')
    return redirect('aAbout')

# ===================================================================== end about admin
# ===================================================================== start panel support
@user_passes_test(support_only, login_url='/accounts/login/')
@check_position([2])
def eSupport(request):
    return render(request, 'registration/support/e_support.html')

# ===================================================================== end panel support
# ===================================================================== start panel registration
@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def eProductRegistration(request):
    product_count = ProductModel.objects.all().count()
    category_count = CategoryModel.objects.all().count()
    add_images_product_form = AddImagesProductForm()
    add_product_form = AddProductForm()
    gallery_product_model = GalleryProductModel.objects.all()
    edit_product_form = EditProductForm()
    ticket_PR = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_registration/e_product_registration.html', {
        'product_count':product_count,
        'category_count':category_count,
        'add_images_product_form':add_images_product_form,
        'add_product_form':add_product_form,
        'gallery_product_model':gallery_product_model,
        'edit_product_form':edit_product_form,
        'ticket_PR':ticket_PR
    })

# ===================================================================== end panel product registration
# ===================================================================== start product registration
@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def prProducts(request):
    products = ProductModel.objects.all()
    add_images_product_form = AddImagesProductForm()
    add_product_form = AddProductForm()
    gallery_product_model = GalleryProductModel.objects.all()
    edit_product_form = EditProductForm()
    ticket_PR = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_registration/e_products.html', {
        'products':products,
        'add_images_product_form':add_images_product_form,
        'add_product_form':add_product_form,
        'gallery_product_model':gallery_product_model,
        'edit_product_form':edit_product_form,
        'ticket_PR':ticket_PR
    })

def prAddProduct(request):
    if request.method == 'POST':
        add_product_form_full = AddProductForm(request.POST, request.FILES)
        if add_product_form_full.is_valid():
            name_product = add_product_form_full.cleaned_data['name']
            price_product = add_product_form_full.cleaned_data['price']
            category_product = add_product_form_full.cleaned_data['category']
            description_product = add_product_form_full.cleaned_data['description']
            image_product = request.FILES['image']
            is_sale_product = add_product_form_full.cleaned_data['is_sale']
            sale_price_product = add_product_form_full.cleaned_data['sale_price']
            number_product = add_product_form_full.cleaned_data['number']
            state_product = add_product_form_full.cleaned_data['state']
            new_product = ProductModel(name=name_product, price=price_product, category=category_product, description=description_product, is_sale=is_sale_product, sale_price=sale_price_product, image=image_product, number=number_product, state=state_product)
            new_product.save()
            messages.success(request, 'این محصول با موفقیت ثبت شد')
            return redirect('prProducts')
        else:
            messages.success(request, add_product_form_full.errors)
            return redirect('prProducts')
    else:
        return redirect('prProducts')

def prAddImagesProduct(request, id_product):
    if request.method == 'POST':
        if GalleryProductModel.objects.count() >= 4:
            messages.success(request, 'شما فقط می توانید 4 تصویر برای هر محصول اضافه کنید.')
            return redirect('prProducts')
        else:
            add_images_product_form_full = AddImagesProductForm(request.POST, request.FILES)
            if add_images_product_form_full.is_valid():
                image = add_images_product_form_full.cleaned_data['image']
                images_product = GalleryProductModel(image=image, product_id=id_product)
                images_product.save()
                messages.success(request, 'تصویر با موفقیت با گالری اضافه شد.')
                return redirect('prProducts')
            else:
                messages.error(request, add_images_product_form_full.errors)
                return redirect('prProducts')
    else:
        return redirect('prProducts')

def prDeleteImages(request, id_image):
    image_find = GalleryProductModel.objects.filter(id=id_image).first()
    image_find.delete()
    messages.success(request, 'تصویر با موفقیت حذف شد.')

    return redirect('prProducts')

def prEditProduct(request, id_product):
    if request.method == 'POST':
        edit_product_form_full = EditProductForm(request.POST, request.FILES)
        if edit_product_form_full.is_valid():
            edit_product_find = ProductModel.objects.filter(id=id_product).first()
            edit_product_find.name = edit_product_form_full.cleaned_data['name']
            edit_product_find.price = edit_product_form_full.cleaned_data['price']
            edit_product_find.category = edit_product_form_full.cleaned_data['category']
            edit_product_find.description = edit_product_form_full.cleaned_data['description']
            if 'image' in request.FILES:
                edit_product_find.image = request.FILES['image']
            edit_product_find.is_sale = edit_product_form_full.cleaned_data['is_sale']
            edit_product_find.sale_price = edit_product_form_full.cleaned_data['sale_price']
            edit_product_find.state = edit_product_form_full.cleaned_data['state']
            edit_product_find.save()
            messages.success(request, 'این محصول با موفقیت ویرایش شد.')
            return redirect('prProducts')
        else:
            messages.success(request, edit_product_form_full.errors)
            return redirect('prEditProduct', id_product)
    else:
        return redirect('prEditProduct', id_product)

def prDeleteProduct(request, id_product):
    delete_product = ProductModel.objects.filter(id=id_product).first()
    delete_product.delete()
    messages.success(request, 'حدف محصول با موفقیت انجام شد.')
    return redirect('prProducts')

# ===================================================================== end product product registration
# ===================================================================== start product registration category
@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def prCategory(request):
    categorys = CategoryModel.objects.all()
    add_category_form = AddCategoryForm()
    edit_category_form = EditCategoryForm()
    ticket_PR = TicketModel.objects.filter(receive=2, state=1).all()

    return render(request, 'registration/product_registration/e_category.html', {
        'categorys':categorys,
        'add_category_form':add_category_form,
        'edit_category_form':edit_category_form,
        'ticket_PR':ticket_PR
    })

def prAddCategory(request):
    if request.method == 'POST':
        add_category_form_full = AddCategoryForm(data=request.POST)
        if add_category_form_full.is_valid():
            category_name = add_category_form_full.cleaned_data['category_name']
            new_category = CategoryModel(name=category_name)
            new_category.save()
            messages.success(request, 'دسته مورد نظر با موفقیت اضافه شد.')
            return redirect('prCategory')
        else:
            messages.success(request, add_category_form_full.errors)
            return redirect('prCategory')
    else:
        return redirect('prCategory')

def prDeleteCategory(request, id_category):
    delete_category = CategoryModel.objects.filter(id=id_category).first()
    delete_category.delete()
    messages.success(request, 'حدف دسته با موفقیت انجام شد.')
    return redirect('prCategory')

def prEditCategory(request, id_category):
    if request.method == 'POST':
        name = request.POST.get('name')
        find_category = CategoryModel.objects.filter(id=id_category).first()
        find_category.name = name
        find_category.save()
        messages.success(request, 'ویرایش دسته با موفقیت انجام شد.')
        return redirect('prCategory')
    else:
        return redirect('prCategory')

# ===================================================================== end product registration category
# ===================================================================== start product registration advertising
@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def prMainAvertising(request):
    advertising_form = AdvertisingForm()
    advertisings_show = AdvertisingModel.objects.all()
    edit_advertising_form = EditAdvertisingForm()
    ticket_PR = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_registration/e_advertising.html', {
        'advertising_form':advertising_form,
        'advertisings_show':advertisings_show,
        'edit_advertising_form':edit_advertising_form,
        'ticket_PR':ticket_PR
    })

def prAddMainAdvertising(request):
    if request.method == 'POST':
        if AdvertisingModel.objects.count() >= 4:
            messages.success(request, 'شما فقط می توانید 4 تصویر تبلیغاتی اضافه کنید.')
            return redirect('prMainAvertising')
        else:
            add_advertising_form_full = AdvertisingForm(request.POST, request.FILES)
            if add_advertising_form_full.is_valid():
                text_advertising = add_advertising_form_full.cleaned_data['text']
                image_advertising = request.FILES['image']
                title_advertising = add_advertising_form_full.cleaned_data['title']
                description_advertising = add_advertising_form_full.cleaned_data['description']
                new_advertising = AdvertisingModel(text=text_advertising, image=image_advertising, title=title_advertising, description=description_advertising)
                new_advertising.save()
                messages.success(request, 'تبلیغات با موفقیت اضافه شد.')
                return redirect('prMainAvertising')
            else:
                messages.success(request, add_advertising_form_full.errors)
                return redirect('prMainAvertising')
    else:
        return redirect('prMainAvertising')

def prEditMainAdvertising(request, id_advertising):
    if request.method == 'POST':
        edit_advertising_form = EditAdvertisingForm(request.POST, request.FILES)
        if edit_advertising_form.is_valid():
            advertising_find = AdvertisingModel.objects.filter(id=id_advertising).first()
            advertising_find.text = edit_advertising_form.cleaned_data['text']
            if 'image' in request.FILES:
                advertising_find.image = request.FILES['image']
            advertising_find.title = edit_advertising_form.cleaned_data['title']
            advertising_find.description = edit_advertising_form.cleaned_data['description']
            advertising_find.save()
            messages.success(request, 'ویرایش با موفقیت انجام شد.')
            return redirect('prMainAvertising')
        else:
            messages.success(request, edit_advertising_form.errors)
            return redirect('prMainAvertising')
    else:
        return render('prMainAvertising')
    
def prDeleteAdvertising(request, id_advertising):
    delete_advertising = AdvertisingModel.objects.filter(id=id_advertising).first()
    delete_advertising.delete()
    messages.success(request, 'حذف تبلیغ با موفقیت انجام شد.')
    return redirect('prMainAvertising')

# ===================================================================== end product registration advertising
# ===================================================================== start product registration discount code
@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def prDiscountCode(request):
    all_discount_code = DiscountCodeModel.objects.all()
    for discount_code in all_discount_code:
        discount_code.shamsi_start_date = jdatetime.datetime.fromgregorian(datetime=discount_code.start_date).strftime('%Y/%m/%d')
        discount_code.shamsi_end_date = jdatetime.datetime.fromgregorian(datetime=discount_code.end_date).strftime('%Y/%m/%d')
    discount_code_form = DiscountCodeForm()
    edit_discount_code_form = EditDiscountCodeForm()
    ticket_PR = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()
    
    return render(request, 'registration/product_registration/e_discount_code.html', {
        'all_discount_code':all_discount_code,
        'discount_code_form':discount_code_form,
        'edit_discount_code_form':edit_discount_code_form,
        'ticket_PR':ticket_PR
    })

def prAddDiscountCode(request):
    if request.method == 'POST':
        discount_code_form_full = DiscountCodeForm(request.POST)
        if discount_code_form_full.is_valid():
            discount_code = discount_code_form_full.cleaned_data['discount_code']
            discount_percent = discount_code_form_full.cleaned_data['discount_percent']
            description = discount_code_form_full.cleaned_data['description']
            end_date = discount_code_form_full.cleaned_data['end_date']
            is_active = discount_code_form_full.cleaned_data['is_active']
            new_discount_code = DiscountCodeModel(discount_code=discount_code, discount_percent=discount_percent, description=description, end_date=end_date, is_active=is_active)
            new_discount_code.save()
            messages.success(request, 'کد تخفیف اضافه شد.')
            return redirect('prDiscountCode')
        else:
            messages.error(request, discount_code_form_full.errors)
            return redirect('prDiscountCode')
    else:
        return redirect('prDiscountCode')

def prEditDiscountCode(request, id_discountCode):
    if request.method == 'POST':
        find_discount_code = DiscountCodeModel.objects.filter(id=id_discountCode).first()
        edit_discount_code_form = EditDiscountCodeForm(request.POST, instance=find_discount_code)
        if edit_discount_code_form.is_valid():
            edit_discount_code_form.save()
            messages.success(request, 'کد تخفیف با موفقیت ویرایش شد.')
            return redirect('prDiscountCode')
        else:
            messages.error(request, edit_discount_code_form.errors)
            return redirect('prDiscountCode')
    else:
        return redirect('prDiscountCode')

def prDeleteDiscountCode(request, id_discountCode):
    delete_discount_code = ProductModel.objects.filter(id=id_discountCode).first()
    delete_discount_code.delete()
    messages.success(request, 'حدف کد تخفیف با موفقیت انجام شد.')
    return redirect('prDiscountCode')

# ===================================================================== end product registration discount code
# ===================================================================== start product registration info
@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def infoPR(request):
    edit_info_form = EditInfoForm()
    edit_username_form = EditUsernameForm()
    edit_password_form = EditPasswordForm()
    ticket_PR = TicketModel.objects.filter(receive=2, state=1).all()

    return render(request, 'registration/product_registration/info_product_registration.html', {
        'edit_info_form':edit_info_form,
        'edit_username_form':edit_username_form,
        'edit_password_form':edit_password_form,
        'ticket_PR':ticket_PR
    })

def editPR(request, id_employee):
    if request.method == 'POST':
        edit_form_full = EditInfoForm(request.POST, request.FILES)
        if edit_form_full.is_valid():
            admin_find = UserModel.objects.filter(id=id_employee).first()
            admin_find.first_name = edit_form_full.cleaned_data['first_name']
            admin_find.last_name = edit_form_full.cleaned_data['last_name']
            admin_find.email = edit_form_full.cleaned_data['email']
            admin_find.phone = edit_form_full.cleaned_data['phone']
            admin_find.address = edit_form_full.cleaned_data['address']
            if 'image' in request.FILES:
                admin_find.image = request.FILES['image']
            admin_find.save()
            messages.success(request, 'ویرایش با موفقیت انجام شد.')
            return redirect('infoPR')
        else:
            messages.success(request, edit_form_full.errors)
            return redirect('infoPR')
    else:
        return redirect('infoPR')

def editUsernamePR(request, id_employee):
    if request.method == 'POST':
        change_username_form = EditUsernameForm(request.POST)
        if change_username_form.is_valid():
            user_find = UserModel.objects.filter(id=id_employee).first()
            user_find.username = change_username_form.cleaned_data['username']
            user_find.save()
            messages.success(request, 'نام کاربری با موفقیت ویرایش شد.')
            return redirect('infoPR')
        else:
            messages.error(request, change_username_form.errors)
            return redirect('infoPR')
    else:
        return redirect('infoPR')

def editPasswordPR(request, id_employee):
    if request.method == 'POST':
        change_password_form = EditPasswordForm(request.POST)
        if change_password_form.is_valid():
            password1 = change_password_form.cleaned_data['password1']
            password2 = change_password_form.cleaned_data['password2']
            if password1 == password2:
                user_find = UserModel.objects.filter(id=id_employee).first()
                user_find.set_password(password1)
                user_find.save()
                login(request, user_find)
                messages.success(request, 'رمز عبور کاربر با موفقیت ویرایش شد.')
                return redirect('infoPR')
            else:
                messages.error(request, 'رمز عبور با هم تطابق ندارد.')
                return redirect('infoPR')
        else:
            messages.error(request, change_password_form.errors)
            return redirect('infoPR')
    else:
        return redirect('infoPR')
    
# ========================================= end product registration about
# ========================================= start product registration ticket
@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def ticketPR(request, id_PR):
    ticket_receive_admin = TicketModel.objects.filter(receive_id=id_PR).all()
    ticket_send_admin = TicketModel.objects.filter(send_id=id_PR).all()
    users = UserModel.objects.all()
    reply_ticket_form = ReplyTicketForm()
    send_ticket_admin_form = SendTicketAdminForm()
    ticket_PR = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_registration/ticket_product_registration.html', {
        'ticket_receive_admin':ticket_receive_admin,
        'ticket_send_admin':ticket_send_admin,
        'users':users,
        'reply_ticket_form':reply_ticket_form,
        'send_ticket_admin_form':send_ticket_admin_form,
        'ticket_PR':ticket_PR
    })

@user_passes_test(product_registration_only, login_url='/accounts/login/')
@check_position([3])
def showTicketPR(request, id_ticket):
    all_categorys = CategoryModel.objects.all()
    users = UserModel.objects.all()
    ticket_show = TicketModel.objects.filter(id=id_ticket).first()
    replay_ticket_form = ReplyTicketForm()
    show_replay_ticket = ReplayTicketModel.objects.filter(ticket_id=id_ticket).all()

    if ticket_show:
        ticket_show.shamsi_date_ticket = jdatetime.datetime.fromgregorian(datetime=ticket_show.created).strftime('%Y/%m/%d')
    
    for replay in show_replay_ticket:
        replay.shamsi_date_replay_ticket = jdatetime.datetime.fromgregorian(datetime=replay.created).strftime('%Y/%m/%d')

    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_registration/e_show_ticket.html', {
        'all_categorys':all_categorys,
        'users':users,
        'ticket_show':ticket_show,
        'replay_ticket_form':replay_ticket_form,
        'show_replay_ticket':show_replay_ticket,
        'ticket_admin':ticket_admin,
    })

def replayTicketPR(request, id_PR, id_ticket):
    if request.method == 'POST':
        text = request.POST.get('text')
        ticket_find = TicketModel.objects.filter(id=id_ticket).first()
        if ticket_find:
            ticket_find.state = 0
            ticket_find.save()
            sender = UserModel.objects.get(id=id_PR)
            ticket_add = ReplayTicketModel(replay_text=text, ticket=ticket_find, sender=sender)
            ticket_add.save()
            messages.success(request, 'پاسخ تیکت با موفقیت ارسال شد.')
            return redirect('showTicketPR', id_ticket)
        else:
            messages.error(request, 'تیکت مورد نظر یافت نشد..')
            return redirect('showTicketPR', id_ticket)
    else:
        return redirect('showTicketPR', id_ticket)

# ========================================= end product registration ticket
# ========================================= start panel eFinance
@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def eFinance(request):
    ticket_finance = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/finance/e_finance.html', {
        'ticket_finance':ticket_finance
    })

def infoF(request):
    edit_info_form = EditInfoForm()
    edit_username_form = EditUsernameForm()
    edit_password_form = EditPasswordForm()
    ticket_finance = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/finance/info_finance.html', {
        'edit_info_form':edit_info_form,
        'edit_username_form':edit_username_form,
        'edit_password_form':edit_password_form,
        'ticket_finance':ticket_finance
    })

def editF(request, id_employee):
    if request.method == 'POST':
        edit_form_full = EditInfoForm(request.POST, request.FILES)
        if edit_form_full.is_valid():
            admin_find = UserModel.objects.filter(id=id_employee).first()
            admin_find.first_name = edit_form_full.cleaned_data['first_name']
            admin_find.last_name = edit_form_full.cleaned_data['last_name']
            admin_find.email = edit_form_full.cleaned_data['email']
            admin_find.phone = edit_form_full.cleaned_data['phone']
            admin_find.address = edit_form_full.cleaned_data['address']
            if 'image' in request.FILES:
                admin_find.image = request.FILES['image']
            admin_find.save()
            messages.success(request, 'ویرایش با موفقیت انجام شد.')
            return redirect('infoF')
        else:
            messages.success(request, edit_form_full.errors)
            return redirect('infoF')
    else:
        return redirect('infoF')

def editUsernameF(request, id_employee):
    if request.method == 'POST':
        change_username_form = EditUsernameForm(request.POST)
        if change_username_form.is_valid():
            user_find = UserModel.objects.filter(id=id_employee).first()
            user_find.username = change_username_form.cleaned_data['username']
            user_find.save()
            messages.success(request, 'نام کاربری با موفقیت ویرایش شد.')
            return redirect('infoF')
        else:
            messages.error(request, change_username_form.errors)
            return redirect('infoF')
    else:
        return redirect('infoF')

def editPasswordF(request, id_employee):
    if request.method == 'POST':
        change_password_form = EditPasswordForm(request.POST)
        if change_password_form.is_valid():
            password1 = change_password_form.cleaned_data['password1']
            password2 = change_password_form.cleaned_data['password2']
            if password1 == password2:
                user_find = UserModel.objects.filter(id=id_employee).first()
                user_find.set_password(password1)
                user_find.save()
                login(request, user_find)
                messages.success(request, 'رمز عبور کاربر با موفقیت ویرایش شد.')
                return redirect('infoF')
            else:
                messages.error(request, 'رمز عبور با هم تطابق ندارد.')
                return redirect('infoF')
        else:
            messages.error(request, change_password_form.errors)
            return redirect('infoF')
    else:
        return redirect('infoF')
    
# ===================================================================== end panel eFinance
# ===================================================================== start buy factor
@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def fBuyFactors(request):
    factor_show = FactorModel.objects.all()
    for factor in factor_show:
        factor.shamsi_date = jdatetime.datetime.fromgregorian(datetime=factor.buy_data).strftime('%Y/%m/%d')

    ticket_finance = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/finance/e_buy_factors.html', {
        'factor_show':factor_show,
        'ticket_finance':ticket_finance
    })

@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def fShowProductsUser(request, id_factor):
    factor_product_show =  FactorProductModel.objects.filter(factor_id=id_factor).all()
    for product in factor_product_show:
        product.shamsi_buy_date = jdatetime.datetime.fromgregorian(datetime=product.factor.buy_data).strftime('%Y/%m/%d')

    return render(request, 'registration/finance/e_show_products_user.html', {
        'factor_product_show':factor_product_show
    })

# ===================================================================== end buy factor
# ===================================================================== start finance products
@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def fProducts(request):
    products = ProductModel.objects.all()
    edit_product_price_form = EditProductForm()
    ticket_finance = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/finance/e_products.html', {
        'products':products,
        'edit_product_price_form':edit_product_price_form,
        'ticket_finance':ticket_finance
    })

def fEditProductPrice(request, id_product):
    if request.method == 'POST':
        edit_product_form_full = EditProductPrice(request.POST, request.FILES)
        if edit_product_form_full.is_valid():
            edit_product_find = ProductModel.objects.filter(id=id_product).first()
            edit_product_find.price = edit_product_form_full.cleaned_data['price']
            edit_product_find.is_sale = edit_product_form_full.cleaned_data['is_sale']
            edit_product_find.sale_price = edit_product_form_full.cleaned_data['sale_price']
            edit_product_find.save()
            messages.success(request, 'این محصول با موفقیت قیمت گذاری شد.')
            return redirect('fProducts')
        else:
            messages.success(request, edit_product_form_full.errors)
            return redirect('fProducts')
    else:
        return redirect('fProducts')

# ===================================================================== end finance products
# ===================================================================== start finance Employee Right
@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def fEmployeeRight(request):
    employees = UserModel.objects.filter(is_staff=True, is_superuser=False)
    for employee in employees:
        employee.shamsi_date_joined = jdatetime.datetime.fromgregorian(datetime=employee.date_joined).strftime('%Y/%m/%d')
    set_employee_right_form = setEmployeeRightForm()
    ticket_finance = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/finance/e_employee_right.html', {
        'employees':employees,
        'set_employee_right_form':set_employee_right_form,
        'ticket_finance':ticket_finance
    })

def fEditEmployee(request, id_employee):
    if request.method == 'POST':
        set_employee_right_form = setEmployeeRightForm(request.POST)
        if set_employee_right_form.is_valid():
            set_employee_right_find = UserModel.objects.filter(id=id_employee).first()
            set_employee_right_find.right = set_employee_right_form.cleaned_data['right']
            set_employee_right_find.save()
            messages.success(request, 'ویرایش حقوق با موفقیت انجام شد.')
            return redirect('fEmployeeRight')
        else:
            messages.error(request, set_employee_right_form.errors)
            return redirect('fEmployeeRight')
    else:
        return redirect('fEmployeeRight')
    
# ========================================= end finance Employee Right
# ========================================= start finance bank transactions
@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def fBankTransactions(request):
    transactions = Bank.objects.all()
    for transaction in transactions:
        transaction.shamsi_date = jdatetime.datetime.fromgregorian(datetime=transaction.created_at).strftime('%Y/%m/%d')
    
    ticket_finance = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/finance/e_bank_transactions.html', {
        'transactions':transactions,
        'ticket_finance':ticket_finance
    })
    
# ========================================= end finance bank transactions
# ========================================= start finance ticket
@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def ticketFinance(request, id_finance):
    ticket_receive_admin = TicketModel.objects.filter(receive_id=id_finance).all()
    ticket_send_admin = TicketModel.objects.filter(send_id=id_finance).all()
    users = UserModel.objects.all()
    reply_ticket_form = ReplyTicketForm()
    send_ticket_admin_form = SendTicketAdminForm()
    ticket_finance = TicketModel.objects.filter(receive_id=id_finance, state=1).all()

    return render(request, 'registration/finance/ticket_finance.html', {
        'ticket_receive_admin':ticket_receive_admin,
        'ticket_send_admin':ticket_send_admin,
        'users':users,
        'reply_ticket_form':reply_ticket_form,
        'send_ticket_admin_form':send_ticket_admin_form,
        'ticket_finance':ticket_finance
    })

@user_passes_test(finance_only, login_url='/accounts/login/')
@check_position([4])
def showTicketFinance(request, id_ticket):
    all_categorys = CategoryModel.objects.all()
    users = UserModel.objects.all()
    ticket_show = TicketModel.objects.filter(id=id_ticket).first()
    replay_ticket_form = ReplyTicketForm()
    show_replay_ticket = ReplayTicketModel.objects.filter(ticket_id=id_ticket).all()

    if ticket_show:
        ticket_show.shamsi_date_ticket = jdatetime.datetime.fromgregorian(datetime=ticket_show.created).strftime('%Y/%m/%d')
    
    for replay in show_replay_ticket:
        replay.shamsi_date_replay_ticket = jdatetime.datetime.fromgregorian(datetime=replay.created).strftime('%Y/%m/%d')

    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/finance/e_show_ticket.html', {
        'all_categorys':all_categorys,
        'users':users,
        'ticket_show':ticket_show,
        'replay_ticket_form':replay_ticket_form,
        'show_replay_ticket':show_replay_ticket,
        'ticket_admin':ticket_admin
    })

def replayTicketFinance(request, id_finance, id_ticket):
    if request.method == 'POST':
        text = request.POST.get('text')
        ticket_find = TicketModel.objects.filter(id=id_ticket).first()
        if ticket_find:
            ticket_find.state = 0
            ticket_find.save()
            sender = UserModel.objects.get(id=id_finance)
            ticket_add = ReplayTicketModel(replay_text=text, ticket=ticket_find, sender=sender)
            ticket_add.save()
            messages.success(request, 'پاسخ تیکت با موفقیت ارسال شد.')
            return redirect('showTicketPR', id_ticket)
        else:
            messages.error(request, 'تیکت مورد نظر یافت نشد..')
            return redirect('showTicketPR', id_ticket)
    else:
        return redirect('showTicketPR', id_ticket)

# ========================================= end finance ticket
# ========================================= start panel product post
@user_passes_test(product_post_only, login_url='/accounts/login/')
@check_position([5])
def eProductPost(request):
    ticket_PP = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_post/e_product_post.html', {
        'ticket_PP':ticket_PP
    })

@user_passes_test(product_post_only, login_url='/accounts/login/')
@check_position([5])
def ppBuyFactors(request):
    factor_show = FactorModel.objects.all()
    for factor in factor_show:
        factor.shamsi_date = jdatetime.datetime.fromgregorian(datetime=factor.buy_data).strftime('%Y/%m/%d')

    ticket_PP = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_post/e_buy_factors.html', {
        'factor_show':factor_show,
        'ticket_PP':ticket_PP
    })

@user_passes_test(product_post_only, login_url='/accounts/login/')
@check_position([5])
def ppShowProductsUser(request, id_factor):
    factor_product_show =  FactorProductModel.objects.filter(factor_id=id_factor).all()
    for product in factor_product_show:
        product.shamsi_buy_date = jdatetime.datetime.fromgregorian(datetime=product.factor.buy_data).strftime('%Y/%m/%d')

    return render(request, 'registration/product_post/e_show_products_user.html', {
        'factor_product_show':factor_product_show
    })

@user_passes_test(product_post_only, login_url='/accounts/login/')
@check_position([5])
def infoPP(request):
    edit_info_form = EditInfoForm()
    edit_username_form = EditUsernameForm()
    edit_password_form = EditPasswordForm()
    ticket_PP = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_post/info_product_post.html', {
        'edit_info_form':edit_info_form,
        'edit_username_form':edit_username_form,
        'edit_password_form':edit_password_form,
        'ticket_PP':ticket_PP
    })

def editPP(request, id_employee):
    if request.method == 'POST':
        edit_form_full = EditInfoForm(request.POST, request.FILES)
        if edit_form_full.is_valid():
            admin_find = UserModel.objects.filter(id=id_employee).first()
            admin_find.first_name = edit_form_full.cleaned_data['first_name']
            admin_find.last_name = edit_form_full.cleaned_data['last_name']
            admin_find.email = edit_form_full.cleaned_data['email']
            admin_find.phone = edit_form_full.cleaned_data['phone']
            admin_find.address = edit_form_full.cleaned_data['address']
            if 'image' in request.FILES:
                admin_find.image = request.FILES['image']
            admin_find.save()
            messages.success(request, 'ویرایش با موفقیت انجام شد.')
            return redirect('infoPP')
        else:
            messages.success(request, edit_form_full.errors)
            return redirect('infoPP')
    else:
        return redirect('infoPP')

def editUsernamePP(request, id_employee):
    if request.method == 'POST':
        change_username_form = EditUsernameForm(request.POST)
        if change_username_form.is_valid():
            user_find = UserModel.objects.filter(id=id_employee).first()
            user_find.username = change_username_form.cleaned_data['username']
            user_find.save()
            messages.success(request, 'نام کاربری با موفقیت ویرایش شد.')
            return redirect('infoPP')
        else:
            messages.error(request, change_username_form.errors)
            return redirect('infoPP')
    else:
        return redirect('infoPP')

def editPasswordPP(request, id_employee):
    if request.method == 'POST':
        change_password_form = EditPasswordForm(request.POST)
        if change_password_form.is_valid():
            password1 = change_password_form.cleaned_data['password1']
            password2 = change_password_form.cleaned_data['password2']
            if password1 == password2:
                user_find = UserModel.objects.filter(id=id_employee).first()
                user_find.set_password(password1)
                user_find.save()
                login(request, user_find)
                messages.success(request, 'رمز عبور کاربر با موفقیت ویرایش شد.')
                return redirect('infoPP')
            else:
                messages.error(request, 'رمز عبور با هم تطابق ندارد.')
                return redirect('infoPP')
        else:
            messages.error(request, change_password_form.errors)
            return redirect('infoPP')
    else:
        return redirect('infoPP')

# ========================================= start product post ticket
@user_passes_test(product_post_only, login_url='/accounts/login/')
@check_position([5])
def ticketPP(request, id_PP):
    ticket_receive_admin = TicketModel.objects.filter(receive_id=id_PP).all()
    ticket_send_admin = TicketModel.objects.filter(send_id=id_PP).all()
    users = UserModel.objects.all()
    reply_ticket_form = ReplyTicketForm()
    send_ticket_admin_form = SendTicketAdminForm()
    ticket_PP = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_post/ticket_product_post.html', {
        'ticket_receive_admin':ticket_receive_admin,
        'ticket_send_admin':ticket_send_admin,
        'users':users,
        'reply_ticket_form':reply_ticket_form,
        'send_ticket_admin_form':send_ticket_admin_form,
        'ticket_PP':ticket_PP
    })

@user_passes_test(product_post_only, login_url='/accounts/login/')
@check_position([5])
def showTicketPP(request, id_ticket):
    all_categorys = CategoryModel.objects.all()
    users = UserModel.objects.all()
    ticket_show = TicketModel.objects.filter(id=id_ticket).first()
    replay_ticket_form = ReplyTicketForm()
    show_replay_ticket = ReplayTicketModel.objects.filter(ticket_id=id_ticket).all()

    if ticket_show:
        ticket_show.shamsi_date_ticket = jdatetime.datetime.fromgregorian(datetime=ticket_show.created).strftime('%Y/%m/%d')
    
    for replay in show_replay_ticket:
        replay.shamsi_date_replay_ticket = jdatetime.datetime.fromgregorian(datetime=replay.created).strftime('%Y/%m/%d')

    ticket_admin = TicketModel.objects.filter(receive_id=request.user.id, state=1).all()

    return render(request, 'registration/product_post/e_show_ticket.html', {
        'all_categorys':all_categorys,
        'users':users,
        'ticket_show':ticket_show,
        'replay_ticket_form':replay_ticket_form,
        'show_replay_ticket':show_replay_ticket,
        'ticket_admin':ticket_admin
    })

def replayTicketPP(request, id_PP, id_ticket):
    if request.method == 'POST':
        text = request.POST.get('text')
        ticket_find = TicketModel.objects.filter(id=id_ticket).first()
        if ticket_find:
            ticket_find.state = 0
            ticket_find.save()
            sender = UserModel.objects.get(id=id_PP)
            ticket_add = ReplayTicketModel(replay_text=text, ticket=ticket_find, sender=sender)
            ticket_add.save()
            messages.success(request, 'پاسخ تیکت با موفقیت ارسال شد.')
            return redirect('showTicketPR', id_ticket)
        else:
            messages.error(request, 'تیکت مورد نظر یافت نشد..')
            return redirect('showTicketPR', id_ticket)
    else:
        return redirect('showTicketPR', id_ticket)
# ========================================= end product post ticket