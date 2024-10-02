from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('loginRegisterUser/', views.loginRegisterUser, name='loginRegisterUser'),

    path('loginUser/', views.loginUser, name='loginUser'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    path('registerUser/', views.registerUser, name='registerUser'),

    path('search/', views.search, name='search'),
    path('autocomplete_search/', views.autocomplete_search, name='autocomplete_search'),
    
    path('profileUser/<int:id_user>/', views.profileUser, name='profileUser'),
    path('editProfileUser/<int:id_user>/', views.editProfileUser, name='editProfileUser'),
    path('editUsername/<int:id_user>/', views.editUsername, name='editUsername'),
    path('editPassword/<int:id_user>/', views.editPassword, name='editPassword'),
    
    path('sendTicket/<int:id_user>/', views.sendTicket, name='sendTicket'),
    path('showTicket/<int:id_ticket>/', views.showTicket, name='showTicket'),
    path('deleteTicket/<int:id_ticket>/<int:id_user>/', views.deleteTicket, name='deleteTicket'),
    path('replayTicket/<int:id_ticket>/<int:id_user>/', views.replayTicket, name='replayTicket'),

    path('shop/', views.shop, name='shop'),
    path('filterShop/', views.filterShop, name='filterShop'),

    path('allProducts/', views.allProducts, name='allProducts'),
    path('allSaleProducts/', views.allSaleProducts, name='allSaleProducts'),
    path('productDetails/<int:id_product>/', views.productDetails, name='productDetails'),
    
    path('productLike/<int:id_product>/', views.productLike, name='productLike'),
    path('productDisLike/<int:id_product>/', views.productDisLike, name='productDisLike'),

    path('satisfactionAdd/<int:id_product>/<int:id_user>/', views.satisfactionAdd, name='satisfactionAdd'),
    
    path('commentAdd/<int:id_product>/<int:id_user>/', views.commentAdd, name='commentAdd'),
    path('replayCommentAdd/<int:id_product>/<int:id_user>/<int:id_comment>/', views.replayCommentAdd, name='replayCommentAdd'),
    
    path('productBuy/<int:id_product>/', views.productBuy, name='productBuy'),
    path('myCart/', views.myCart, name='myCart'),
    path('plusQTY/<int:id_product>/', views.plusQTY, name='plusQTY'),
    path('minusQTY/<int:id_product>/', views.minusQTY, name='minusQTY'),
    path('myCartDelete/<int:id_product>/', views.myCartDelete, name='myCartDelete'),
    path('reviewProductsCart/', views.reviewProductsCart, name='reviewProductsCart'),
    path('editProfileUserCart/<int:id_user>/', views.editProfileUserCart, name='editProfileUserCart'),

    path('discountCodeAccep/', views.discountCodeAccep, name='discountCodeAccep'),
    path('discountCodeDelete/', views.discountCodeDelete, name='discountCodeDelete'),

    path('allCategory/', views.allCategory, name='allCategory'),
    path('allProductsCategory/<int:id_category>/', views.allProductsCategory, name='allProductsCategory'),
    path('allBestSellerProducts/', views.allBestSellerProducts, name='allBestSellerProducts'),


    path('about/', views.about, name='about'),
    path('support/', views.support, name='support'),
]

urlpatterns += [
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done",),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm",),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete",),
]