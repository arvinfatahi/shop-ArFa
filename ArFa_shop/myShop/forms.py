from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserModel, TicketModel, BrandModel, FactorModel

# ================================================== function
def validate_phone_number(value):
    if not value.isdigit() or len(value) != 11:
        raise ValidationError('شماره تلفن باید 11 رقم و فقط شامل اعداد باشد.')

# ================================================== contact form
class SupportForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'موضوع'}))
    section = forms.CharField(widget=forms.Select(attrs={'class':'form-control'}))

# ================================================== price form
class FilterForm(forms.Form):
    min_price = forms.CharField(required=False, min_length=4, max_length=7, widget=forms.TextInput(attrs={'class':'txt-min-price', 'id':'txt-min-price', 'placeholder':'حداقل قیمت 1000 هزار تومان'}))
    max_price = forms.CharField(required=False, min_length=4, max_length=7, widget=forms.TextInput(attrs={'class':'txt-max-price', 'id':'txt-max-price', 'placeholder':'حداکثر قیمت 5 میلیون تومان'}))
    sale = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'chk-sale', 'id':'filter-sale'}))
    state = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'chk-state', 'id':'filter-state'}))
    not_price = 0
    min_to_max = 1
    max_to_min = 2
    choice_order = (
        (not_price, 'بدون مرتب سازی'),
        (min_to_max, 'کمترین به بیشترین قیمت'),
        (max_to_min, 'بیشترین به کمترین قیمت'),
    )
    order = forms.ChoiceField(choices=choice_order, widget=forms.Select(attrs={'class':'cmb-select-order'}))

# ================================================== login form 
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری', 'style':'text-align: center;'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control mt-3', 'placeholder':'رمز عبور', 'style':'text-align: center;'}),
        required=True
    )

# ================================================== register form 
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری', 'style':'text-align: center;'}),
        required=True
    )
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'class':'form-control mt-3', 'placeholder':'شماره موبایل', 'style':'text-align: center;'}),
        required=True
    )
    password1 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control mt-3', 'placeholder':'رمز عبور', 'style':'text-align: center;'}),
        required=True
    )
    password2 = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class':'form-control mt-3', 'placeholder':'رمز عبور مجدد', 'style':'text-align: center;'}),
        required=True
    )
    
    class Meta:
        model = UserModel
        fields = ['username', 'phone', 'password1', 'password2']

# ================================================== TicketForm
class TicketForm(forms.ModelForm):
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
    section = forms.ChoiceField(choices=select_position, widget=forms.Select(attrs={'class':'ticket-section'}))
    subject = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs={'class':'ticket-subject', 'placeholder':'موضوع تیکت'}))
    text = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={'class':'ticket-text', 'placeholder':'متن تیکت'}))

    class Meta:
        model = TicketModel
        fields = ['text']

# ================================================== EditProfileUserForm
class EditProfileUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'txt-first-name', 'placeholder':'نام'}))
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'txt-last-name', 'placeholder':'نام خانوادگی'}))
    phone = forms.CharField(required=True, max_length=11, validators=[validate_phone_number], widget=forms.TextInput(attrs={'class':'txt-phone', 'placeholder':'تلفن'}))
    email = forms.EmailField(max_length=200, required=False, widget=forms.EmailInput(attrs={'class':'txt-email', 'placeholder':'ایمیل'}))
    choice_province = (
        ('آذربایجان شرقی', 'آذربایجان شرقی'), ('آذربایجان غربی', 'آذربایجان غربی'), ('اردبیل', 'اردبیل'), ('اصفهان', 'اصفهان'), ('البرز', 'البرز'), ('ایلام', 'ایلام'),
        ('بوشهر', 'بوشهر'), ('تهران', 'تهران'), ('چهارمحال و بختیاری', 'چهارمحال و بختیاری'), ('خراسان جنوبی', 'خراسان جنوبی'), ('خراسان رضوی', 'خراسان رضوی'),
        ('خراسان شمالی', 'خراسان شمالی'), ('خوزستان', 'خوزستان'), ('زنجان', 'زنجان'), ('سمنان', 'سمنان'), ('سیستان و بلوچستان', 'سیستان و بلوچستان'), ('فارس', 'فارس'),
        ('قزوین', 'قزوین'), ('قم', 'قم'), ('کردستان', 'کردستان'), ('کرمان', 'کرمان'), ('کرمانشاه', 'کرمانشاه'), ('کهکیلویه و بویراحمد', 'کهکیلویه و بویراحمد'),
        ('گلستان', 'گلستان'), ('گیلان', 'گیلان'), ('لرستان', 'لرستان'), ('مازندران', 'مازندران'), ('مرکزی', 'مرکزی'), ('هرمزگان', 'هرمزگان'), ('همدان', 'همدان'), ('یزد', 'یزد'),
    )
    province = forms.ChoiceField(choices=choice_province, widget=forms.Select(attrs={'class':'txt-province'}))
    city = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'txt-city', 'placeholder':'شهر'}))
    address = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={'class':'txt-address', 'placeholder':'آدرس (شامل خیابان و ... )'}))

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'phone', 'email', 'province', 'city', 'address']

# ================================================== EditProfileUserUsernameForm
class EditProfileUserUsernameForm(forms.ModelForm):
    username = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs={'class':'txt-customer-username', 'placeholder':'نام کاربری'}))

    class Meta:
        model = UserModel
        fields = ['username']

# ================================================== EditProfileUserPasswordForm
class EditProfileUserPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'txt-customer-password', 'placeholder':'رمز عبور'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'txt-customer-re-password', 'placeholder':'تکرار رمز عبور'}))

# ================================================== SearchForm
class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-search', 'id':'txt-search', 'placeholder':'جستجوی محصول'}))

# ================================================== DiscountCodeForm
class DiscountCodeForm(forms.Form):
    discount_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class':'txt-discount-code', 'placeholder':'کد تخفیف'}))

# ================================================== FactorForm
class FactorForm(forms.ModelForm):
    no = 0
    yes = 1
    choice_factor = (
        (no, 'خیر'),
        (yes, 'بله')
    )
    is_factor = forms.ChoiceField(choices=choice_factor, widget=forms.Select(attrs={'class': 'sel-is-factor'}))

    class Meta:
        model = FactorModel
        fields = '__all__'

# ================================================== replayTicketForm
class ReplayTicketForm(forms.Form):
    replay_text = forms.CharField(max_length=10000, required=True, widget=forms.Textarea(attrs={'class':'txt-replay-ticket', 'placeholder':'پاسخ به تیکت ...'}))