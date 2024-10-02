from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.exceptions import ValidationError
from azbankgateways.models import Bank
from django_jalali.db.models import jDateField

# Create your models here.
class UserModel(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    province = models.CharField(max_length=50, verbose_name='استان', null=True)
    city = models.CharField(max_length=80, verbose_name='شهر', null=True)
    address = models.CharField(max_length=500, verbose_name='آدرس', blank=True)

    admin = 1
    support = 2
    product_registration = 3
    accountants = 4
    product_post = 5
    select_position = (
        (admin, 'مدیر'),
        (support, 'پشتیبان'),
        (product_registration, 'ثبت کالا'),
        (accountants, 'حسابدار'),
        (product_post, 'پست کالا')
    )
    position = models.IntegerField(choices=select_position, verbose_name='سمت و پست کارمند', null=True, blank=True)
    image = models.ImageField(upload_to='profileImage/', verbose_name='تصویر پروفایل', null=True, blank=True)
    right = models.DecimalField(max_digits=11, decimal_places=0, verbose_name='حقوق', null=True, blank=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

class CategoryModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='نام دسته')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته‌ها'

class ProductModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12, verbose_name='قیمت محصول')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name='دسته بندی محصول')
    description = models.TextField(verbose_name='توضیح محصول', blank=True)
    image = models.ImageField(upload_to='productImage/', verbose_name='تصویر محصول')
    is_sale = models.BooleanField(verbose_name='محصول دارای تخفیف', blank=True)
    sale_price = models.DecimalField(decimal_places=0, max_digits=12, verbose_name='قیمت تخفیف خورده', null=True, blank=True)
    number = models.IntegerField(default=1, verbose_name='تعداد محصول')
    slider = models.BooleanField(default=False, verbose_name='انتخاب اسلاید', blank=True)
    state = models.BooleanField(default=True, verbose_name='موجودی محصول')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
    
    def clean(self):
        if self.slider:
            slider_count = ProductModel.objects.filter(slider=True).count()
            if slider_count >= 4:
                raise ValidationError("فقط می‌توانید ۴ محصول را به عنوان اسلاید انتخاب کنید.")

class SatisfactionModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    satisfaction = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='میزان رضایت')

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name = 'رضایت از محصول'
        verbose_name_plural = 'رضایت از محصولات'

class CommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    comment_text = models.TextField(verbose_name='متن نظر')
    published_comment = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

class ReplayCommentModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, verbose_name='نظر')
    comment_text = models.TextField(verbose_name='متن نظر')
    published_comment = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ریپلای نظر'
        verbose_name_plural = 'ریپلای نظرات'

class GalleryProductModel(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='GalleryProduct/', verbose_name='تصویر محصولات')

    class Meta:
        verbose_name = 'گالری تصویر'
        verbose_name_plural = 'گالری تصاویر'

class BrandModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='نام برند')
    image = models.ImageField(upload_to='brandImage/', verbose_name='عکس')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'

class CartModel(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    number = models.IntegerField(verbose_name='تعداد محصول در سبد خرید')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خریدها'

class FactorModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ManyToManyField(ProductModel, through='FactorProductModel', verbose_name='محصول')
    bank_transaction = models.OneToOneField(Bank, on_delete=models.CASCADE, verbose_name='تراکنش بانکی', null=True)
    is_factor = models.IntegerField(verbose_name='صادر کردن فاکتور', null=True)
    buy_data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتورها'

class FactorProductModel(models.Model):
    factor = models.ForeignKey(FactorModel, on_delete=models.CASCADE, verbose_name='فاکتور')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    number = models.IntegerField(verbose_name='تعداد محصول')

    class Meta:
        verbose_name = 'محصولات فاکتور'
        verbose_name_plural = 'محصولات فاکتورها'

class TicketModel(models.Model):
    id = models.AutoField(primary_key=True)
    receive = models.ForeignKey(UserModel, related_name='received_tickets', on_delete=models.CASCADE, verbose_name='کاربر دریافت کننده پیام')
    send = models.ForeignKey(UserModel, related_name='sent_tickets', on_delete=models.CASCADE, verbose_name='کاربر ارسال کننده پیام')
    subject = models.CharField(verbose_name='موضوع تیکت', max_length=100, null=True)
    text = models.TextField(verbose_name='متن تیکت')
    state = models.IntegerField(verbose_name='وضعیت تیکت', default=1)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'

class ReplayTicketModel(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE, verbose_name='تیکت')
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='ارسال کننده', null=True)  # باید ForeignKey باشد
    replay_text = models.TextField(verbose_name='متن ریپلای')
    created = models.DateTimeField(auto_now_add=True, null=True)

class PageViewModel(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class LikeModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    like = models.IntegerField(verbose_name='لایک')

class disLikeModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='محصول')
    disLike = models.IntegerField(verbose_name='دیس لایک')

class AdvertisingModel(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200, verbose_name='متن تبلیغات')
    image = models.ImageField(upload_to='advertisingImage/' ,verbose_name='عکس تبلیغات', blank=True)
    title = models.CharField(max_length=100, verbose_name='عنوان تبلیغات')
    description = models.CharField(max_length=500, verbose_name='توضیحات')

class DiscountCodeModel(models.Model):
    id = models.AutoField(primary_key=True)
    discount_code = models.CharField(max_length=10, unique=True, verbose_name='کد تخفیف')
    discount_percent = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(100)], max_digits=5, decimal_places=2, verbose_name='درصد تخفیف')
    description = models.CharField(max_length=200, verbose_name='توضیحات', null=True)
    start_date = models.DateTimeField(default=timezone.now, verbose_name='شروع تاریخ')
    # end_date = models.DateTimeField(verbose_name='پایان تاریخ')
    end_date = jDateField(null=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن تخفیف')

    def __str__(self):
        return self.discount_code

    def is_valid(self):
        return self.is_active and self.start_date <= timezone.now() <= self.end_date

class AboutModel(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='aboutImage/', verbose_name='تصویر کاربر')
    about = models.TextField(verbose_name='توضیح کاربر')
    