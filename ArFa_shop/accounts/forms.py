from django import forms
from myShop.models import (
    ProductModel,
    CategoryModel,
    UserModel,
    BrandModel,
    AdvertisingModel,
    DiscountCodeModel,
    AboutModel
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django_jalali.forms import jDateField
from django_jalali.admin.widgets import AdminjDateWidget

class EditEmployeeAdminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class':'form-control'}))
    
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
    position = forms.ChoiceField(choices=select_position, widget=forms.Select(attrs={'class':'form-select'}))
    
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'image', 'phone', 'address', 'position', 'is_superuser', 'is_staff']

# -------------------------------------------------- AddEmployeeForm
class AddEmployeeForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-employee-username', 'placeholder':'نام کاربری'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'txt-employee-password', 'placeholder':'رمز عبور'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'txt-employee-re-password', 'placeholder':'تکرار رمز عبور'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-employee-first-name', 'placeholder':'نام'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-employee-last-name', 'placeholder':'نام خانوادگی'}))
    support = 2
    product_registration = 3
    accountants = 4
    product_post = 5
    select_position = (
        (support, 'پشتیبان'),
        (product_registration, 'ثبت کالا'),
        (accountants, 'مالی'),
        (product_post, 'پست کالا')
    )
    position = forms.ChoiceField(choices=select_position, widget=forms.Select(attrs={'class':'cmb-employee-position'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'txt-employee-email', 'placeholder':'ایمیل'}))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'txt-employee-phone', 'placeholder':'تلفن'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class':'txt-employee-address', 'placeholder':'آدرس'})) 
    right = forms.DecimalField(widget=forms.TextInput(attrs={'class':'txt-employee-right', 'placeholder':'حقوق'}))
    is_staff = forms.BooleanField(initial=True, widget=forms.HiddenInput(attrs={'class': 'txt-employee-staff'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'img-employee-profile', 'style':'margin-bottom:20px'}))

    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'position', 'email', 'phone', 'address', 'right', 'is_staff', 'image']

# -------------------------------------------------- EditEmployeeForm
class EditEmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-employee-first-name', 'id':'edit-employee-first-name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-employee-last-name', 'id':'edit-employee-last-name'}))
    support = 2
    product_registration = 3
    accountants = 4
    product_post = 5
    select_position = (
        (support, 'پشتیبان'),
        (product_registration, 'ثبت کالا'),
        (accountants, 'مالی'),
        (product_post, 'پست کالا')
    )
    position = forms.ChoiceField(required=True, choices=select_position, widget=forms.Select(attrs={'class':'cmb-employee-position', 'id':'edit-employee-position'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'txt-employee-email', 'id':'edit-employee-email'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'img-employee-select-image'}))
    phone = forms.CharField(required=True, max_length=11, widget=forms.TextInput(attrs={'class':'txt-employee-phone', 'id':'edit-employee-phone'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class':'txt-employee-address', 'id':'edit-employee-address'}))
    right = forms.DecimalField(widget=forms.TextInput(attrs={'class':'txt-employee-right', 'id':'edit-employee-right', 'placeholder':'حقوق'}))
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'image', 'phone', 'address', 'right']

# -------------------------------------------------- setEmployeeRightForm
class setEmployeeRightForm(forms.Form):
    right = forms.DecimalField(required=True, widget=forms.TextInput(attrs={'class':'txt-employee-right', 'id':'edit-employee-right', 'placeholder':'حقوق', 'style':'margin-bottom:10px;'}))

# -------------------------------------------------- AddCategoryForm
class AddCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class':'txt-category-name', 'placeholder':'نام دسته', 'style':'margin-bottom:15px;'}))

    class Meta:
        model = UserModel
        fields = ['right']

# -------------------------------------------------- EditCategoryForm
class EditCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class':'txt-category-name', 'id':'edit-category-name', 'placeholder':'نام دسته', 'style':'margin-bottom:15px;'}))
    
    class Meta:
        model = CategoryModel
        fields = '__all__'

# -------------------------------------------------- AddBrandForm
class AddBrandForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class':'txt-brand-name', 'placeholder':'نام برند'}))
    image = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class':'img-brand', 'style':'margin-bottom:15px;'}))

# -------------------------------------------------- EditBrandForm
class EditBrandForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class':'txt-brands-name', 'id':'edit-brands-name', 'placeholder':'نام برند'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'img-brands'}))

    class Meta:
        model = BrandModel
        fields = '__all__'

# -------------------------------------------------- AddImagesProductForm
class AddImagesProductForm(forms.Form):
    image = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class':'img-product', 'style':'margin-bottom:15px'}))

# -------------------------------------------------- AddProductForm
class AddProductForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-product-name', 'placeholder':'نام محصول'}))
    price = forms.DecimalField(max_digits=10, widget=forms.NumberInput(attrs={'class':'txt-product-price', 'placeholder':'قیمت محصول'}))
    category = forms.ModelChoiceField(queryset=CategoryModel.objects.all(), widget=forms.Select(attrs={'class':'cmb-product-category mb-2'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'txt-product-description', 'placeholder':'درباره محصول', 'style':'resize: none; height:100px;'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'img-product'}))
    is_sale = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chk-product-sale'}))
    sale_price = forms.DecimalField(required=False, max_digits=10, widget=forms.NumberInput(attrs={'class':'txt-sale_price'}))
    number = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'txt-product-number'}))
    slider = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chk-slider'}))
    state = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chk-product-state'}))

    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'category', 'description', 'image', 'is_sale', 'sale_price', 'state']

# -------------------------------------------------- EditProductForm
class EditProductForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-product-name', 'id':'edit-product-name'}))
    price = forms.DecimalField(max_digits=10, widget=forms.NumberInput(attrs={'class':'txt-product-price', 'id':'edit-product-price'}))
    category = forms.ModelChoiceField(queryset=CategoryModel.objects.all(), widget=forms.Select(attrs={'class':'cmb-product-category', 'id':'edit-product-category'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'txt-product-description', 'id':'edit-product-description', 'style':'resize: none; height:100px;'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'img-product'}))
    is_sale = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chk-product-sale', 'id':'edit-product-sale'}))
    sale_price = forms.DecimalField(required=False, max_digits=10, widget=forms.NumberInput(attrs={'class':'txt-sale_price', 'id':'edit-product-sale-price'}))
    number = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'txt-product-number', 'id':'edit-product-number'}))
    slider = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chk-product-slider', 'id':'edit-product-slider'}))
    state = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chk-product-state', 'id':'edit-product-state'}))

    class Meta:
        model = ProductModel
        fields = '__all__'

# -------------------------------------------------- EditUserForm
class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-users-fName', 'id':'edit-users-fName'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-users-lName', 'id':'edit-users-lName'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'txt-users-email', 'id':'edit-users-email'}))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'txt-users-phone', 'id':'edit-users-phone'}))
    address = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'class':'txt-users-address', 'id':'edit-users-address', 'style':'resize: none; height:100px;'}))
    
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

# -------------------------------------------------- EditInfoForm
class EditInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-info-admin-fName', 'id':'edit-info-admin-fName'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-info-admin-lName', 'id':'edit-info-admin-lName'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class':'txt-info-admin-email', 'id':'edit-info-admin-email'}))
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'txt-info-admin-phone', 'id':'edit-info-admin-phone'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class':'txt-info-admin-address', 'id':'edit-info-admin-address'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'img-info-admin', 'id':'edit-img-info-admin'}))

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'image']

# --------------------------------------------------  EditPasswordForm
class EditPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'txt-users-password', 'placeholder':'رمز عبور جدید'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'txt-users-rePassword', 'placeholder':'تکرار رمز عبور جدید', 'style':'margin-bottom:15px;'}))

# -------------------------------------------------- EditUsernameForm
class EditUsernameForm(forms.ModelForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'txt-users-username', 'id':'edit-users-username', 'placeholder':'نام کاربری جدید', 'style':'margin-bottom:15px;'}))
    
    class Meta:
        model = UserModel
        fields = ['username']

# -------------------------------------------------- ReplyTicketAdminForm
class ReplyTicketForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'txt-replay-ticket', 'placeholder':'پاسخ به تیکت','style':'margin-bottom:15px;'}))

# -------------------------------------------------- SendTicketAdminForm
class SendTicketAdminForm(forms.Form):
    support = 2
    product_registration = 3
    accountants = 4
    product_post = 5
    select_position = (
        (support, 'پشتیبان'),
        (product_registration, 'ثبت کالا'),
        (accountants, 'حسابدار'),
        (product_post, 'پست کالا')
    )
    section = forms.ChoiceField(choices=select_position, widget=forms.Select(attrs={'class':'select-section'}))
    subject = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class':'txt-subject', 'placeholder':'موضوع تیکت'}))
    txtTicket = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'txt-ticket', 'placeholder':'متن تیکت'}))

# =================================================== AdvertisingForm
class AdvertisingForm(forms.ModelForm):
    text = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class':'txt-text-advertising', 'placeholder':'متن تبلیغات'}))
    image = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class':'img-image-advertising'}))
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'txt-title-advertising', 'placeholder':'عنوان تبلیغات'}))
    description = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'class':'txt-description-advertising', 'placeholder':'توضیحات', 'style':'margin-bottom:15px;'}))

    class Meta:
        model = AdvertisingModel
        fields = '__all__'
# ================================================== EditAdvertisingForm
class EditAdvertisingForm(forms.Form):
    text = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class':'txt-text-advertising', 'id':'txt-text-advertising', 'placeholder':'زیر عنوان'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'img-select-image-advertising', 'id':'img-select-image-advertising'}))
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class':'txt-title-advertising', 'id':'txt-title-advertising', 'placeholder':'عنوان تبلیغات'}))
    description = forms.CharField(max_length=500, required=True, widget=forms.TextInput(attrs={'class':'txt-description-advertising', 'id':'txt-description-advertising', 'placeholder':'توضیحات', 'style':'margin-bottom:15px;'}))

# =================================================== DiscountCodeForm
class DiscountCodeForm(forms.ModelForm):
    discount_code = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class':'txt-discount-code', 'placeholder':'کد تخفیف'}))
    discount_percent = forms.DecimalField(max_digits=5, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class':'txt-discount-percent', 'placeholder':'درصد تخفیف'}))
    description = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class':'txt-description', 'placeholder':'توضیحات'}))
    # end_date = forms.DateField(widget=forms.DateInput(attrs={'class':'discount-date', 'type':'text'}))
    end_date = jDateField(widget=AdminjDateWidget())
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chb-is-active'}))

    class Meta:
        model = DiscountCodeModel
        fields = ['discount_code', 'discount_percent', 'description', 'end_date', 'is_active']

# =================================================== EditDiscountCodeForm
class EditDiscountCodeForm(forms.ModelForm):
    discount_code = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class':'txt-discount-code', 'id':'edit-discount-code'}))
    discount_percent = forms.DecimalField(max_digits=5, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class':'txt-discount-percent', 'id':'edit-discount-percent'}))
    description = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class':'txt-description', 'id':'edit-description'}))
    # end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class':'end-date', 'id':'edit-end-date', 'type':'date'}))
    end_date = jDateField(widget=AdminjDateWidget())
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chb-is-active', 'id':'edit-is-active'}))

    class Meta:
        model = DiscountCodeModel
        fields = ['discount_code', 'discount_percent', 'description', 'end_date', 'is_active']

# =================================================== AddAboutForm
class AddAboutForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'img-about-members'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class':'txt-about-members', 'placeholder':'درباره اعضا', 'style':'height:100px; resize: none; margin-bottom: 10px;'}))

    class Meta:
        model = AboutModel
        fields = '__all__'

# =================================================== AddAboutForm
class EditAboutForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'img-about-members', 'id':'img-about-members'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class':'txt-about-members', 'id':'edit-about-members', 'placeholder':'درباره اعضا', 'style':'height:100px; resize: none; margin-bottom: 10px;'}))

    class Meta:
        model = AboutModel
        fields = '__all__'

# =================================================== EditProductPrice
class EditProductPrice(forms.Form):
    price = forms.DecimalField(max_digits=10, widget=forms.NumberInput(attrs={'class':'txt-product-price', 'id':'edit-product-price'}))
    is_sale = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'chk-product-sale', 'id':'edit-product-sale'}))
    sale_price = forms.DecimalField(required=False, max_digits=10, widget=forms.NumberInput(attrs={'class':'txt-sale_price', 'id':'edit-product-sale-price'}))
