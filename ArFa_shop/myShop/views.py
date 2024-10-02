from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from decimal import Decimal
from django.template.loader import render_to_string
import jdatetime
from datetime import datetime

from .models import (
    ProductModel,
    AdvertisingModel,
    CategoryModel,
    UserModel, 
    TicketModel,
    ReplayTicketModel,
    SatisfactionModel,
    CommentModel,
    ReplayCommentModel,
    LikeModel,
    disLikeModel,
    BrandModel,
    GalleryProductModel,
    DiscountCodeModel,
    AboutModel,
    PageViewModel
    )
from .forms import (
    RegisterForm,
    LoginForm,
    TicketForm,
    EditProfileUserForm,
    EditProfileUserUsernameForm,
    EditProfileUserPasswordForm,
    SupportForm,
    FilterForm,
    SearchForm,
    DiscountCodeForm,
    FactorForm,
    ReplayTicketForm,
    )

# Create your views here.
def index(request):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    all_categorys = CategoryModel.objects.all()
    search_form = SearchForm()
    slider = ProductModel.objects.filter(slider=True).all()
    products = ProductModel.objects.all()
    new_products = ProductModel.objects.all().order_by('-created')[:8]
    advertising_show = AdvertisingModel.objects.all()
    sale_products = ProductModel.objects.filter(is_sale=True).all()
    brands = BrandModel.objects.all()
    # PageViewModel.objects.create()
    # visit_count = PageViewModel.objects.count()
    
    return render(request, 'index.html', {
        'discount_code_model_show':discount_code_model_show,
        'all_categorys':all_categorys,
        'search_form':search_form,
        'slider':slider,
        'products':products,
        'new_products':new_products,
        'advertising_show':advertising_show,
        'green':'green',
        'red':'red',
        'purple':'purple',
        'blue':'blue',
        'sale_products':sale_products,
        'brands':brands
        # 'visit_count':visit_count
    })

def loginRegisterUser(request):
    register_form = RegisterForm()
    login_form = LoginForm()
    return render(request, 'loginRegisterUser.html', {
        'register_form':register_form,
        'login_form':login_form
    })

def loginUser(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        username = login_form.data['username']
        password = login_form.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'کاربری با این مشخصات وجود ندارد.')
            return redirect('loginRegisterUser')
    else:
        return redirect('loginRegisterUser')

def logoutUser(request):
    logout(request)
    return redirect('index')

def registerUser(request):
    if request.method == 'POST':
        register_form_full = RegisterForm(data=request.POST)
        if register_form_full.is_valid():
            new_user = register_form_full.save()
            login(request, new_user)
            return redirect('index')
        else:
            messages.error(request, register_form_full.errors)
            return redirect('loginRegisterUser')
    else:
        return redirect('loginRegisterUser')

def search(request):
    if request.method == 'POST':
        discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
        all_categorys = CategoryModel.objects.all()
        search_form_full = SearchForm(request.POST)
        search = search_form_full.data['search']
        search = search.lstrip()
        search = search.rstrip()
        product_search = ProductModel.objects.filter(name__icontains=search).all()
        
        search_form = SearchForm()

        return render(request, 'search.html', {
            'discount_code_model_show':discount_code_model_show,
            'all_categorys':all_categorys,
            'search':search,
            'product_search':product_search,
            'search_form':search_form
        })
    else:
        return redirect('index')

def autocomplete_search(request):
    if 'term' in request.GET:
        qs = ProductModel.objects.filter(name__icontains=request.GET.get('term'))
        names = list(qs.values('name'))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

# =========================================================== end login and register and search
# =========================================================== start profile
@login_required(login_url='/loginRegisterUser/')
def profileUser(request, id_user):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    user = UserModel.objects.filter(id=id_user).first()
    ticket_form = TicketForm()
    edit_profile_user_form = EditProfileUserForm(instance=user)
    edit_profile_user_username_form = EditProfileUserUsernameForm(instance=user)
    edit_profile_user_password_form = EditProfileUserPasswordForm()
    ticket_send_show = TicketModel.objects.filter(Q(send=id_user)).all()
    ticket_receive_show = TicketModel.objects.filter(Q(receive=id_user)).all()
    ticket_show = TicketModel.objects.filter(Q(send=id_user) & Q(receive=1)).all()

    return render(request, 'profile_user.html', {
        'discount_code_model_show':discount_code_model_show,
        'search_form':search_form,
        'user':user,
        'ticket_form':ticket_form,
        'edit_profile_user_form':edit_profile_user_form,
        'edit_profile_user_username_form':edit_profile_user_username_form,
        'edit_profile_user_password_form':edit_profile_user_password_form,
        'ticket_send_show':ticket_send_show,
        'ticket_receive_show':ticket_receive_show,
        'ticket_show':ticket_show
    })

def editProfileUser(request, id_user):
    if request.method == 'POST':
        edit_profile_user_form = EditProfileUserForm(request.POST)
        if edit_profile_user_form.is_valid():
            user_find = UserModel.objects.filter(id=id_user).first()
            user_find.first_name = edit_profile_user_form.cleaned_data['first_name']
            user_find.last_name = edit_profile_user_form.cleaned_data['last_name']
            user_find.phone = edit_profile_user_form.cleaned_data['phone']
            user_find.email = edit_profile_user_form.cleaned_data['email']
            user_find.province = edit_profile_user_form.cleaned_data['province']
            user_find.city = edit_profile_user_form.cleaned_data['city']
            user_find.address = edit_profile_user_form.cleaned_data['address']
            user_find.save()
            messages.success(request, 'پروفایل با موفقیت ویرایش شد.')
            return redirect('profileUser', id_user)
        else:
            messages.error(request, edit_profile_user_form.errors)
            return redirect('profileUser', id_user)
    else:
        return redirect('profileUser', id_user)

def editUsername(request, id_user):
    if request.method == 'POST':
        edit_profile_user_username_form = EditProfileUserUsernameForm(request.POST)
        if edit_profile_user_username_form.is_valid():
            user_find = UserModel.objects.filter(id=id_user).first()
            user_find.username = edit_profile_user_username_form.cleaned_data['username']
            user_find.save()
            messages.success(request, 'نام کاربری با موفقیت ویرایش شد.')
            return redirect('profileUser', id_user)
        else:
            messages.error(request, edit_profile_user_username_form.errors)
            return redirect('profileUser', id_user)
    else:
        return redirect('profileUser', id_user)

def editPassword(request, id_user):
    if request.method == 'POST':
        edit_profile_user_password_form = EditProfileUserPasswordForm(request.POST)
        if edit_profile_user_password_form.is_valid():
            password1 = edit_profile_user_password_form.cleaned_data['password1']
            password2 = edit_profile_user_password_form.cleaned_data['password2']
            if password1 == password2:
                user_find = UserModel.objects.filter(id=id_user).first()
                user_find.set_password(password1)
                user_find.save()
                messages.success(request, 'رمز عبور با موفقیت ویرایش شد.')
                return redirect('profileUser', id_user)
        else:
            messages.error(request, edit_profile_user_password_form.errors)
            return redirect('profileUser', id_user)
    else:
        return redirect('profileUser', id_user)

def sendTicket(request, id_user):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            receive = ticket_form.cleaned_data['section']
            receive_users = UserModel.objects.filter(position=receive)
            if not receive_users.exists():
                messages.error(request, 'هیچ کاربری با این موقعیت یافت نشد.')
                return redirect('profileUser', id_user)
            send = UserModel.objects.get(id=id_user)
            subject = ticket_form.cleaned_data['subject']
            text = ticket_form.cleaned_data['text']
            state = 1
            for receive in receive_users:
                ticket_add = TicketModel(receive=receive, send=send, subject=subject, text=text, state=state)
                ticket_add.save()
            messages.success(request, 'تیکت با موفقیت ارسال شد و در اسرع وقت پاسخ خود را دریافت خواهید کرد')
            return redirect('profileUser', id_user)
        else:
            messages.error(request, ticket_form.errors)
            return redirect('profileUser', id_user)
    else:
        return redirect('profileUser', id_user)

def showTicket(request, id_ticket):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    all_categorys = CategoryModel.objects.all()
    users = UserModel.objects.all()
    ticket_show = TicketModel.objects.filter(id=id_ticket).first()
    replay_ticket_form = ReplayTicketForm()
    show_replay_ticket = ReplayTicketModel.objects.filter(ticket_id=id_ticket).all()

    return render(request, 'profile/show_ticket.html', {
        'discount_code_model_show':discount_code_model_show,
        'search_form':search_form,
        'all_categorys':all_categorys,
        'users':users,
        'ticket_show':ticket_show,
        'replay_ticket_form':replay_ticket_form,
        'show_replay_ticket':show_replay_ticket
    })

def deleteTicket(request, id_ticket, id_user):
    find_ticket = TicketModel.objects.filter(id=id_ticket).first()
    find_ticket.delete()
    messages.success(request, 'تیکت با موفقین حذف شد.')
    return redirect('profileUser', id_user)

def replayTicket(request, id_ticket, id_user):
    if request.method == 'POST':
        replay_ticket_form = ReplayTicketForm(request.POST)
        if replay_ticket_form.is_valid():
            replay_text = replay_ticket_form.cleaned_data['replay_text']
            replay_ticket = ReplayTicketModel(replay_text=replay_text, ticket_id=id_ticket, sender=id_user)
            replay_ticket.save()
            messages.success(request, 'تیکت با موفقیت ارسال شد.')
            return redirect('show_ticket', id_ticket)
        else:
            messages.error(request, replay_ticket_form.errors)
            return redirect('show_ticket', id_ticket)
    else:
        return redirect('show_ticket', id_ticket)

# =========================================================== end profile
# =========================================================== start shop
def shop(request):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    all_categorys = CategoryModel.objects.all()

    limit = 8 
    offset = int(request.GET.get('offset', 0))

    all_products = ProductModel.objects.all()[offset:offset + limit]

    filter_form = FilterForm()

    # بررسی درخواست AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_html = render_to_string('product_list.html', {'all_products': all_products})
        return JsonResponse({
            'products_html': products_html,
            'has_next': ProductModel.objects.count() > offset + limit,
        })

    return render(request, 'shop.html', {
        'discount_code_model_show': discount_code_model_show,
        'search_form': search_form,
        'all_categorys': all_categorys,
        'all_products': all_products,
        'filter_form': filter_form
    })

def filterShop(request):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    all_categorys = CategoryModel.objects.all()

    filter_form = FilterForm(request.POST or None)
    
    if filter_form.is_valid():
        min_price = filter_form.cleaned_data['min_price']
        max_price = filter_form.cleaned_data['max_price']
        order = filter_form.cleaned_data['order']
        sale = filter_form.cleaned_data['sale']
        state = filter_form.cleaned_data['state']
        
        all_products = ProductModel.objects.all()
        if min_price:
            all_products = all_products.filter(price__gte=min_price)
        if max_price:
            all_products = all_products.filter(price__lte=max_price)
        if sale:
            all_products = all_products.filter(is_sale=True)
        if state:
            all_products = all_products.filter(state__gt=0)
        
        if order == '1':
            all_products = all_products.order_by('price')
        elif order == '2':
            all_products = all_products.order_by('-price')

    else:
        all_products = ProductModel.objects.all()

    limit = 8
    offset = int(request.GET.get('offset', 0))
    all_products = all_products[offset:offset + limit]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_html = render_to_string('product_list.html', {'all_products': all_products})
        return JsonResponse({
            'products_html': products_html,
            'has_next': ProductModel.objects.count() > offset + limit,
        })

    return render(request, 'filter_shop.html', {
        'discount_code_model_show': discount_code_model_show,
        'search_form': search_form,
        'all_categorys': all_categorys,
        'all_products': all_products,
        'filter_form': filter_form
    })

# =========================================================== end shop
# =========================================================== start products
def allProducts(request):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    all_products = ProductModel.objects.all()
    all_categorys = CategoryModel.objects.all()
    paginator = Paginator(all_products, 12)
    page = request.GET.get('page')
    all_products = paginator.get_page(page)

    return render(request, 'all_products.html', {
        'discount_code_model_show':discount_code_model_show,
        'search_form':search_form,
        'all_products':all_products,
        'all_categorys':all_categorys,
        'paginator':paginator
    })

def allSaleProducts(request):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    sale_products = ProductModel.objects.filter(is_sale=True).all()
    all_categorys = CategoryModel.objects.all()
    paginator = Paginator(sale_products, 12)
    page = request.GET.get('page')
    all_sale_products = paginator.get_page(page)

    return render(request, 'all_sale_products.html', {
        'discount_code_model_show':discount_code_model_show,
        'search_form':search_form,
        'all_sale_products':all_sale_products,
        'all_categorys':all_categorys
    })

def productDetails(request, id_product):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    all_categorys = CategoryModel.objects.all()
    satisfaction_count = SatisfactionModel.objects.filter(product_id=id_product).count()
    total_amount = SatisfactionModel.objects.filter(product_id=id_product).aggregate(Sum('satisfaction'))
    if total_amount['satisfaction__sum'] is None:
        satisfaction_sum = 0
    else:
        satisfaction_sum = total_amount['satisfaction__sum']
    if satisfaction_count == 0:
        satisfaction_percent = 0
    else:
        satisfaction_percent = satisfaction_sum / satisfaction_count

    product = ProductModel.objects.filter(id=id_product).first()
    gallery_product = GalleryProductModel.objects.filter(product_id=id_product).all()
    id_users = UserModel.objects.all().values_list('id', flat=True).all()
    id_comments = CommentModel.objects.all().values_list('id', flat=True).all()

    # نظرات
    comment_show = CommentModel.objects.filter(product_id=id_product, user_id__in=id_users).all()
    for comment in comment_show:
        comment.shamsi_published_comment = jdatetime.datetime.fromgregorian(datetime=comment.published_comment).strftime('%Y/%m/%d')

    # پاسخ‌ها
    replay_comment_show = ReplayCommentModel.objects.filter(product_id=id_product, user_id__in=id_users, comment_id__in=id_comments).all()
    for replay_comment in replay_comment_show:
        replay_comment.shamsi_published_comment = jdatetime.datetime.fromgregorian(datetime=replay_comment.published_comment).strftime('%Y/%m/%d')

    category = CategoryModel.objects.filter(id=product.category_id).first()
    likes_product = ProductModel.objects.filter(id=id_product).annotate(likes_count=Count('likemodel')).all()
    dis_likes_product = ProductModel.objects.filter(id=id_product).annotate(dis_likes_count=Count('dislikemodel')).all()
    similar_products = ProductModel.objects.filter(category=product.category).exclude(id=product.id)

    return render(request, 'product_details.html', {
        'discount_code_model_show': discount_code_model_show,
        'search_form': search_form,
        'all_categorys': all_categorys,
        'satisfaction_count': satisfaction_count,
        'satisfaction_percent': satisfaction_percent,
        'product': product,
        'gallery_product': gallery_product,
        'comment_show': comment_show,
        'replay_comment_show': replay_comment_show,
        'category': category,
        'likes_product': likes_product,
        'dis_likes_product': dis_likes_product,
        'similar_products': similar_products
    })



def productLike(request, id_product):
    if request.user.is_authenticated:
        if not LikeModel.objects.filter(product_id=id_product, user_id=request.user.id).exists():
            like_add = LikeModel(product_id=id_product, user_id=request.user.id, like=1)
            like_add.save()
            return redirect('productDetails', id_product)
        else:
            messages.error(request, 'شما این محصول را قبلا پسندیده اید.')
            return redirect('productDetails', id_product)
    else:
        messages.error(request, 'لطفا برای لایک کردن این محصول وارد سایت شوید.')
        return redirect('productDetails', id_product)

def productDisLike(request, id_product):
    if request.user.is_authenticated:
        if not disLikeModel.objects.filter(product_id=id_product, user_id=request.user.id).exists():
            like_add = disLikeModel(product_id=id_product, user_id=request.user.id, disLike=1)
            like_add.save()
            return redirect('productDetails', id_product)
        else:
            messages.error(request, 'شما این محصول را قبلا پسندیده اید.')
            return redirect('productDetails', id_product)
    else:
        messages.error(request, 'لطفا برای لایک کردن این محصول وارد سایت شوید.')
        return redirect('productDetails', id_product)

def satisfactionAdd(request, id_product, id_user):
    if request.method == 'POST':
        satisfaction_exists = SatisfactionModel.objects.filter(user_id=id_user).exists()
        if satisfaction_exists:
            messages.success(request, 'یک کاربر نمی تواند برای یک محصول دوبار امتیاز بدهد.')
            return redirect('productDetails', id_product)
        else:
            satisfaction = request.POST.get('range_satisfaction')
            satisfactio_add = SatisfactionModel(satisfaction=satisfaction, product_id=id_product, user_id=id_user)
            satisfactio_add.save()
            messages.success(request, 'امتیاز شما با موفقیت ثبت شد.')
            return redirect('productDetails', id_product)
    else:
        return redirect('productDetails', id_product)

def commentAdd(request, id_product, id_user):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment_add = CommentModel(comment_text=comment_text, product_id=id_product, user_id=id_user)
        comment_add.save()
        messages.success(request, 'نظر برای این محصول با موفقیت ثبت شد.')
        return redirect('productDetails', id_product)
    else:
        return redirect('productDetails', id_product)

def replayCommentAdd(request, id_product, id_user, id_comment):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        replay_comment_add = ReplayCommentModel(comment_text=comment_text, product_id=id_product, user_id=id_user, comment_id=id_comment)
        replay_comment_add.save()
        messages.success(request, 'پاسخ نظر با موفقیت داده شد.')
        return redirect('productDetails', id_product)
    else:
        return redirect('productDetails', id_product)
    
# =========================================================== end products
# =========================================================== start my cart
def productBuy(request, id_product):
    find_product = ProductModel.objects.filter(id=id_product).first()
    if find_product:
        product = {
            'id': find_product.id,
            'name': find_product.name,
            'image': find_product.image.url,
            'qty': 1,
            'price':float(find_product.price),
        }
        
        if 'my_cart' not in request.session:
            request.session['my_cart'] = []
        
        cart = request.session['my_cart']
        
        for item in cart:
            if item['id'] == product['id']:
                return JsonResponse({'status': 'productAddTpCartBefore', 'total_items': len(cart)})
        
        cart.append(product)
        request.session['my_cart'] = cart
        
        total_price_ = 0
        total_qty_ = 0
        for item in cart:
            total_price_ += item['price'] * item['qty']
            total_qty_ += item['qty']

        # محاسبه تخفیف و قیمت نهایی
        discount_percent = request.session.get('discount_percent', 0)
        discount_amount = total_price_ * (discount_percent / 100)
        final_price_ = total_price_ - discount_amount
        final_price_ = float(final_price_)

        request.session['total_price_session'] = total_price_
        request.session['total_qty_session'] = total_qty_
        request.session['final_price_session'] = final_price_
        
        request.session['total_items'] = len(cart)
        request.session.modified = True
        return JsonResponse({
            'status': 'productAddToCart',
            'total_items': len(cart),
            'total_price_': total_price_,
            'total_qty_': total_qty_,
            'final_price_': final_price_
        })
    else:
        return JsonResponse({'status': 'productNotFind', 'total_items': len(cart)})

def myCart(request):
    all_categorys = CategoryModel.objects.all()
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    discount_code_form = DiscountCodeForm()
    cart = request.session.get('my_cart')
    if cart:
        total_price_ = 0
        total_qty_ = 0
        for item in cart:
            total_price_ += item['price']
            total_qty_ += item['qty']
        
        if 'total_price_session' not in request.session:
            request.session['total_price_session'] = []
        request.session['total_price_session'] = total_price_

        if 'total_qty_session' not in request.session:
            request.session['total_qty_session'] = []
        request.session['total_qty_session'] = total_qty_
        
        # if 'final_price_session' not in request.session:
        #     request.session['final_price_session'] = []
        # request.session['final_price_session'] = final_price_
        
        request.session.modified = True

        return render(request, 'cart.html', {
            'all_categorys':all_categorys,
            'discount_code_model_show':discount_code_model_show,
            'search_form':search_form,
            'discount_code_form':discount_code_form,
            'total_price_':total_price_,
            'total_qty_':total_qty_
        })
    else:
        return render(request, 'cart.html', {
            'all_categorys':all_categorys,
            'discount_code_model_show':discount_code_model_show,
            'search_form':search_form,
            'discount_code_form':discount_code_form
        })

def plusQTY(request, id_product):
    total_price_ = 0
    total_qty_ = 0
    cart = request.session.get('my_cart')
    
    updated_item_qty = 0
    updated_item_price = 0

    for item in cart:
        if item['id'] == id_product:
            item['qty'] += 1
            item['price'] = item['qty'] * float(ProductModel.objects.get(id=id_product).price)
            updated_item_qty = item['qty']
            updated_item_price = item['price']
        
        total_price_ += item['price']
        total_qty_ += item['qty']

    # محاسبه تخفیف و قیمت نهایی
    discount_percent = request.session.get('discount_percent', [])

    if not discount_percent:
        discount_percent = 0

    discount_amount = total_price_ * (discount_percent / 100)
    final_price_ = total_price_ - discount_amount
    final_price_ = float(final_price_)

    request.session['my_cart'] = cart

    if 'total_price_session' not in request.session:
        request.session['total_price_session'] = []
    request.session['total_price_session'] = total_price_

    if 'total_qty_session' not in request.session:
        request.session['total_qty_session'] = []
    request.session['total_qty_session'] = total_qty_

    if 'final_price_session' not in request.session:
        request.session['final_price_session'] = []
    request.session['final_price_session'] = final_price_
    
    request.session.modified = True

    return JsonResponse({
        'status': 'plusQTYSuccess',
        'QTY': updated_item_qty,
        'price': updated_item_price,
        'total_price_': total_price_,
        'total_qty_': total_qty_,
        'final_price_':final_price_
    })

def minusQTY(request, id_product):
    total_price_ = 0
    total_qty_ = 0
    cart = request.session.get('my_cart')
    
    updated_item_qty = 0
    updated_item_price = 0

    for item in cart:
        if item['id'] == id_product:
            if item['qty'] > 1:
                item['qty'] -= 1
                item['price'] = item['qty'] * float(ProductModel.objects.get(id=id_product).price)
                updated_item_qty = item['qty']
                updated_item_price = item['price']
        
        total_price_ += item['price']
        total_qty_ += item['qty']

    # محاسبه تخفیف و قیمت نهایی
    discount_percent = request.session.get('discount_percent', [])

    if not discount_percent:
        discount_percent = 0

    discount_amount = total_price_ * (discount_percent / 100)
    final_price_ = total_price_ - discount_amount
    final_price_ = float(final_price_)

    request.session['my_cart'] = cart

    if 'total_price_session' not in request.session:
        request.session['total_price_session'] = []
    request.session['total_price_session'] = total_price_

    if 'total_qty_session' not in request.session:
        request.session['total_qty_session'] = []
    request.session['total_qty_session'] = total_qty_

    if 'final_price_session' not in request.session:
        request.session['final_price_session'] = []
    request.session['final_price_session'] = final_price_

    request.session.modified = True

    return JsonResponse({
        'status': 'minusQTYSuccess',
        'QTY': updated_item_qty,
        'price': updated_item_price,
        'total_price_': total_price_,
        'total_qty_': total_qty_,
        'final_price_':final_price_
    })

def myCartDelete(request, id_product):
    total_price_ = 0
    total_qty_ = 0
    cart = request.session.get('my_cart', [])
    
    for item in cart:
        total_price_ += item['qty'] * float(ProductModel.objects.get(id=item['id']).price)
        total_qty_ += item['qty']  

    for item in cart:
        if item['id'] == id_product:
            cart.remove(item)
            product_price = item['qty'] * float(ProductModel.objects.get(id=id_product).price)
            total_price_ -= product_price
            total_qty_ -= item['qty']
            break
            
    request.session['my_cart'] = cart
    request.session['total_items'] = len(cart)

    # محاسبه تخفیف و قیمت نهایی
    discount_percent = request.session.get('discount_percent', [])

    if not discount_percent:
        discount_percent = 0

    discount_amount = total_price_ * (discount_percent / 100)
    final_price_ = total_price_ - discount_amount
    final_price_ = float(final_price_)

    if 'total_price_session' not in request.session:
        request.session['total_price_session'] = []
    request.session['total_price_session'] = total_price_

    if 'total_qty_session' not in request.session:
        request.session['total_qty_session'] = []
    request.session['total_qty_session'] = total_qty_
    
    if 'final_price_session' not in request.session:
        request.session['final_price_session'] = []
    request.session['final_price_session'] = final_price_

    request.session.modified = True

    return JsonResponse({
        'status': 'productDeleteToCart',
        'total_items': len(cart),
        'total_price_':total_price_,
        'total_qty_':total_qty_,
        'final_price_':final_price_,
        'cart_empty': len(cart) == 0
        })

def reviewProductsCart(request):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    factor_form = FactorForm()
    cart = request.session.get('my_cart')
    if cart:
        user = UserModel.objects.filter(id=request.user.id).first()
        edit_profile_user_form = EditProfileUserForm(instance=user)

        return render(request, 'review_products_cart.html', {
            'discount_code_model_show':discount_code_model_show,
            'search_form': search_form,
            'factor_form':factor_form,
            'user':user,
            'edit_profile_user_form':edit_profile_user_form
        })
    else:
        return redirect('index')

def editProfileUserCart(request, id_user):
    if request.method == 'POST':
        edit_profile_user_form = EditProfileUserForm(request.POST)
        if edit_profile_user_form.is_valid():
            user_find = UserModel.objects.filter(id=id_user).first()
            user_find.first_name = edit_profile_user_form.cleaned_data['first_name']
            user_find.last_name = edit_profile_user_form.cleaned_data['last_name']
            user_find.phone = edit_profile_user_form.cleaned_data['phone']
            user_find.email = edit_profile_user_form.cleaned_data['email']
            user_find.province = edit_profile_user_form.cleaned_data['province']
            user_find.city = edit_profile_user_form.cleaned_data['city']
            user_find.address = edit_profile_user_form.cleaned_data['address']
            user_find.save()
            messages.success(request, 'پروفایل با موفقیت ویرایش شد.')
            return redirect('reviewProductsCart')
        else:
            messages.error(request, edit_profile_user_form.errors)
            return redirect('reviewProductsCart')
    else:
        return redirect('reviewProductsCart')

def discountCodeAccep(request):
    if request.method == 'POST':
        discount_code_form_full = DiscountCodeForm(request.POST or None)
        if discount_code_form_full.is_valid():
            code = discount_code_form_full.cleaned_data['discount_code']
            discount_code = DiscountCodeModel.objects.filter(discount_code=code).first()
            if discount_code:
                total_price_ = Decimal(request.POST.get('total_price_'))  # قیمت کل محصولات
                discount_amount = total_price_ * (discount_code.discount_percent / 100)
                final_price = total_price_ - discount_amount
                request.session['final_price_session'] = float(final_price)
                request.session['discount_percent'] = float(discount_code.discount_percent)
                return redirect('myCart')
            else:
                messages.error(request, 'کد تخفیف معتبر نیست.')
                return redirect('myCart')
        else:
            messages.error(request, 'داده های ورودی معتبر نیستن.')
            return redirect('myCart')
    else:
        return redirect('myCart')

def discountCodeDelete(request):
    del request.session['final_price_session']
    return redirect('myCart')

# =========================================================== end my cart
# =========================================================== start categorys
def allCategory(request):
    all_categorys = CategoryModel.objects.all()

    return render(request, 'all_category.html', {
        'all_categorys':all_categorys
    })

def allProductsCategory(request, id_category):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    all_categorys = CategoryModel.objects.all()
    products_category = ProductModel.objects.filter(category_id=id_category).all()
    category_name = CategoryModel.objects.filter(id=id_category).first()

    paginator = Paginator(products_category, 9)
    page = request.GET.get('page')
    products_category = paginator.get_page(page)

    return render(request, 'all_products_category.html', {
        'discount_code_model_show':discount_code_model_show,
        'search_form':search_form,
        'all_categorys':all_categorys,
        'products_category':products_category,
        'category_name':category_name,
        'paginator':paginator
    })

# =========================================================== end categorys
# =========================================================== start all best seller products
def allBestSellerProducts(request):
    return render(request, 'all_best_seller_products.html')

# =========================================================== end all best seller products
# =========================================================== start about
def about(request):
    discount_code_model_show = DiscountCodeModel.objects.filter(is_active=True).first()
    search_form = SearchForm()
    all_categorys = CategoryModel.objects.all()
    about_show = AboutModel.objects.all()

    return render(request, 'about.html', {
        'discount_code_model_show':discount_code_model_show,
        'all_categorys':all_categorys,
        'search_form':search_form,
        'about_show':about_show
    })

def support(request):
    all_categorys = CategoryModel.objects.all()
    support_form = SupportForm()
    
    return render(request, 'support.html', {
        'support_form':support_form,
        'all_categorys':all_categorys
    })
# =========================================================== end about