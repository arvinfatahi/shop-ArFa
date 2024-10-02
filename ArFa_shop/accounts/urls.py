from django.urls import path
from .views import (
    adminPanel,

    infoAdmin,
    editAdmin,
    editPasswordAdmin,
    editUsernameAdmin,

    loginAdmin,
    logoutAdmin,

    aProducts,
    aAddProduct,
    aAddImagesProduct,
    aDeleteImages,
    aEditProduct,
    aDeleteProduct,

    aEmployee,
    aAddEmployee,
    aEditEmployee,
    aDeleteEmployee,
    aSettingEmployee,
    changePassAdminEmployee,
    changeUsernameAdminEmployee,

    aCategory,
    aEditCategory,
    aDeleteCategory,
    aAddCategory,

    aUsers,
    aEditUsers,
    aDeleteUser,
    changePassAdminUser,
    changeUsernameAdminUser,

    aBrand,
    aAddBrand,
    aEditBrand,
    aDeleteBrand,

    ticketAdmin,
    showTicketAdmin,
    deleteTicketAdmin,
    replayTicketAdmin,

    aMainAvertising,
    aAddMainAdvertising,
    aEditMainAdvertising,
    aDeleteAdvertising,

    aDiscountCode,
    aAddDiscountCode,
    aEditDiscountCode,
    aDeleteDiscountCode,

    aBankTransactions,
    aBuyFactors,

    showProductsUser,

    aAbout,
    aAddAboutMembers,
    aEditAboutMembers,
    aDeleteAbout,
# ========================== eSupport
    eSupport,
# ========================== prProductRegistration
    eProductRegistration,

    prProducts,
    prAddProduct,
    prAddImagesProduct,
    prDeleteImages,
    prEditProduct,
    prDeleteProduct,

    prCategory,
    prAddCategory,
    prDeleteCategory,
    prEditCategory,

    prMainAvertising,
    prAddMainAdvertising,
    prEditMainAdvertising,
    prDeleteAdvertising,

    prDiscountCode,
    prAddDiscountCode,
    prEditDiscountCode,
    prDeleteDiscountCode,

    infoPR,
    editPR,
    editUsernamePR,
    editPasswordPR,

    ticketPR,
    showTicketPR,
    replayTicketPR,
# ========================== eFinance
    fProducts,
    fEditProductPrice,

    fEmployeeRight,
    fEditEmployee,
    
    fBankTransactions,

    eFinance,
    fBuyFactors,
    fShowProductsUser,

    infoF,
    editF,
    editUsernameF,
    editPasswordF,

    ticketFinance,
    showTicketFinance,
    replayTicketFinance,
# ========================== ppProductPost
    eProductPost,
    ppBuyFactors,
    ppShowProductsUser,

    infoPP,
    editPP,
    editUsernamePP,
    editPasswordPP,

    ticketPP,
    showTicketPP,
    replayTicketPP,
    )
from django.contrib.auth import views

urlpatterns = [
    
    # path("login/", views.LoginView.as_view(), name="login"),
    path("login/", loginAdmin, name="login"),
    # path("logout/", views.LogoutView.as_view(), name="logout"),
    path('logout/', logoutAdmin, name='logout'),
    # path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    # path("password_change/done/",views.PasswordChangeDoneView.as_view(),name="password_change_done",),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done",),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm",),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete",),
]
urlpatterns += [
    path('', adminPanel, name='adminPanel'),

    path('infoAdmin/', infoAdmin, name='infoAdmin'),
    path('editAdmin/<int:id_admin>/', editAdmin, name='editAdmin'),
    path('editPasswordAdmin/<int:id_admin>/', editPasswordAdmin, name='editPasswordAdmin'),
    path('editUsernameAdmin/<int:id_admin>/', editUsernameAdmin, name='editUsernameAdmin'),

    path('aProducts/', aProducts, name='aProducts'),
    path('aAddProduct/', aAddProduct, name='aAddProduct'),
    path('aAddImagesProduct/<int:id_product>/', aAddImagesProduct, name='aAddImagesProduct'),
    path('aDeleteImages/<int:id_image>/', aDeleteImages, name='aDeleteImages'),
    path('aEditProduct/<int:id_product>/', aEditProduct, name='aEditProduct'),
    path('aDeleteProduct/<int:id_product>/', aDeleteProduct, name='aDeleteProduct'),

    path('aEmployee/', aEmployee, name='aEmployee'),
    path('aAddEmployee/', aAddEmployee, name='aAddEmployee'),
    path('aEditEmployee/<int:id_employee>/', aEditEmployee, name='aEditEmployee'),
    path('aDeleteEmployee/<int:id_employee>/', aDeleteEmployee, name='aDeleteEmployee'),
    path('aSettingEmployee/<int:id_employee>/', aSettingEmployee, name='aSettingEmployee'),
    path('changePassAdminEmployee/<int:id_employee>/', changePassAdminEmployee, name='changePassAdminEmployee'),
    path('changeUsernameAdminEmployee/<int:id_employee>/', changeUsernameAdminEmployee, name='changeUsernameAdminEmployee'),

    path('aUsers/', aUsers, name='aUsers'),
    path('aEditUsers/<int:id_user>', aEditUsers, name='aEditUsers'),
    path('aDeleteUser/<int:id_user>', aDeleteUser, name='aDeleteUser'),
    path('changePassAdminUser/<int:id_user>', changePassAdminUser, name='changePassAdminUser'),
    path('changeUsernameAdminUser/<int:id_user>', changeUsernameAdminUser, name='changeUsernameAdminUser'),
    
    path('aCategory/', aCategory, name='aCategory'),
    path('aAddCategory/', aAddCategory, name='aAddCategory'),
    path('aEditCategory/<int:id_category>/', aEditCategory, name='aEditCategory'),
    path('aDeleteCategory/<int:id_category>/', aDeleteCategory, name='aDeleteCategory'),

    path('aBrand/', aBrand, name='aBrand'),
    path('aAddBrand/', aAddBrand, name='aAddBrand'),
    path('aEditBrand/<int:id_brand>/', aEditBrand, name='aEditBrand'),
    path('aDeleteBrand/<int:id_brand>/', aDeleteBrand, name='aDeleteBrand'),

    path('ticketAdmin/<int:id_admin>/', ticketAdmin, name='ticketAdmin'),
    path('showTicketAdmin/<int:id_ticket>/', showTicketAdmin, name='showTicketAdmin'),
    path('deleteTicketAdmin/<int:id_ticket>/', deleteTicketAdmin, name='deleteTicketAdmin'),
    path('replayTicketAdmin/<int:id_admin>/<int:id_ticket>/', replayTicketAdmin, name='replayTicketAdmin'),
    
    path('aMainAvertising/', aMainAvertising, name='aMainAvertising'),
    path('aAddMainAdvertising/', aAddMainAdvertising, name='aAddMainAdvertising'),
    path('aEditMainAdvertising/<int:id_advertising>/', aEditMainAdvertising, name='aEditMainAdvertising'),
    path('aDeleteAdvertising/<int:id_advertising>/', aDeleteAdvertising, name='aDeleteAdvertising'),

    path('aDiscountCode/', aDiscountCode, name='aDiscountCode'),
    path('aAddDiscountCode/', aAddDiscountCode, name='aAddDiscountCode'),
    path('aEditDiscountCode/<int:id_discountCode>/', aEditDiscountCode, name='aEditDiscountCode'),
    path('aDeleteDiscountCode/<int:id_discountCode>/', aDeleteDiscountCode, name='aDeleteDiscountCode'),

    path('aBankTransactions/', aBankTransactions, name='aBankTransactions'),
    path('aBuyFactors/', aBuyFactors, name='aBuyFactors'),

    path('showProductsUser/<int:id_factor>/', showProductsUser, name='showProductsUser'),

    path('aAbout/', aAbout, name='aAbout'),
    path('aAddAboutMembers/', aAddAboutMembers, name='aAddAboutMembers'),
    path('aEditAboutMembers/<int:id_about>/', aEditAboutMembers, name='aEditAboutMembers'),
    path('aDeleteAbout/<int:id_about>/', aDeleteAbout, name='aDeleteAbout'),
# ========================================================= start support
    path('eSupport/', eSupport, name='eSupport'),
# ========================================================= start product registration
    path('eProductRegistration/', eProductRegistration, name='eProductRegistration'),

    path('infoPR/', infoPR, name='infoPR'),
    path('editPR/<int:id_employee>/', editPR, name='editPR'),
    path('editPasswordPR/<int:id_employee>/', editPasswordPR, name='editPasswordPR'),
    path('editUsernamePR/<int:id_employee>/', editUsernamePR, name='editUsernamePR'),

    path('prProducts/', prProducts, name='prProducts'),
    path('prAddProduct/', prAddProduct, name='prAddProduct'),
    path('prAddImagesProduct<int:id_product>/', prAddImagesProduct, name='prAddImagesProduct'),
    path('prDeleteImages<int:id_image>/', prDeleteImages, name='prDeleteImages'),
    path('prEditProduct/<int:id_product>/', prEditProduct, name='prEditProduct'),
    path('prDeleteProduct/<int:id_product>/', prDeleteProduct, name='prDeleteProduct'),
    
    path('prCategory/', prCategory, name='prCategory'),
    path('prAddCategory/', prAddCategory, name='prAddCategory'),
    path('prDeleteCategory/<int:id_category>/', prDeleteCategory, name='prDeleteCategory'),
    path('prEditCategory/<int:id_category>/', prEditCategory, name='prEditCategory'),

    path('prMainAvertising/', prMainAvertising, name='prMainAvertising'),
    path('prAddMainAdvertising/', prAddMainAdvertising, name='prAddMainAdvertising'),
    path('prEditMainAdvertising/<int:id_advertising>/', prEditMainAdvertising, name='prEditMainAdvertising'),
    path('prDeleteAdvertising/<int:id_advertising>/', prDeleteAdvertising, name='prDeleteAdvertising'),

    path('prDiscountCode/', prDiscountCode, name='prDiscountCode'),
    path('prAddDiscountCode/', prAddDiscountCode, name='prAddDiscountCode'),
    path('prEditDiscountCode/<int:id_discountCode>/', prEditDiscountCode, name='prEditDiscountCode'),
    path('prDeleteDiscountCode/<int:id_discountCode>/', prDeleteDiscountCode, name='prDeleteDiscountCode'),

    path('ticketPR/<int:id_PR>/', ticketPR, name='ticketPR'),
    path('showTicketPR/<int:id_ticket>/', showTicketPR, name='showTicketPR'),
    path('replayTicketPR/<int:id_PR>/<int:id_ticket>/', replayTicketPR, name='replayTicketPR'),
# ========================================================= start eFinance
    path('eFinance/', eFinance, name='eFinance'),
    path('fBuyFactors/', fBuyFactors, name='fBuyFactors'),
    path('fShowProductsUser/<int:id_factor>/', fShowProductsUser, name='fShowProductsUser'),

    path('fProducts/', fProducts, name='fProducts'),

    path('infoF/', infoF, name='infoF'),
    path('editF/', editF, name='editF'),
    path('editUsernameF/<int:id_employee>/', editUsernameF, name='editUsernameF'),
    path('editPasswordF/<int:id_employee>/', editPasswordF, name='editPasswordF'),

    path('fEditProductPrice/<int:id_product>/', fEditProductPrice, name='fEditProductPrice'),

    path('fEmployeeRight/', fEmployeeRight, name='fEmployeeRight'),
    path('fEditEmployee/<int:id_employee>/', fEditEmployee, name='fEditEmployee'),

    path('fBankTransactions/', fBankTransactions, name='fBankTransactions'),

    path('ticketFinance/<int:id_finance>/', ticketFinance, name='ticketFinance'),
    path('showTicketFinance/<int:id_tiket>/', showTicketFinance, name='showTicketFinance'),
    path('replayTicketFinance/<int:id_finance>/<int:id_ticket>/', replayTicketFinance, name='replayTicketFinance'),
# ========================================================= start eProductPost
    path('eProductPost/', eProductPost, name='eProductPost'),
    path('ppBuyFactors/', ppBuyFactors, name='ppBuyFactors'),
    path('ppShowProductsUser/<int:id_factor>/', ppShowProductsUser, name='ppShowProductsUser'),

    path('infoPP/', infoPP, name='infoPP'),
    path('editPP/', editPP, name='editPP'),
    path('editUsernamePP/<int:id_employee>/', editUsernamePP, name='editUsernamePP'),
    path('editPasswordPP/<int:id_employee>/', editPasswordPP, name='editPasswordPP'),

    path('ticketPP/<int:id_PP>/', ticketPP, name='ticketPP'),
    path('showTicketPP/<int:id_PP>/', showTicketPP, name='showTicketPP'),
    path('replayTicketPP/<int:id_PP>/<int:id_ticket>/', replayTicketPP, name='replayTicketPP'),
]