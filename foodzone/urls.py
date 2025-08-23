
from foodapp import views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('register/', views.register, name='register'),
    path('feature/', views.feature, name='feature'),
    path('team/', views.team, name='team'),
    path('menu/', views.menu, name='menu'),
    path('check_user_exists/', views.check_user_exists, name='check_user_exists'),
    path('login/', views.signin, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dishes/',views.all_dishes,name="all_dishes"),
    path('dish/<int:id>/', views.single_dish, name='dish'),
    # path('process-jazzcash-payment/<int:order_id>/', views.process_jazzcash_payment, name='process_jazzcash_payment'),
    # path('buy-dish/<int:id>/', views.buy_dish, name='buy_dish'),
    path('dish/<int:id>/buy/', views.buy_dish, name='buy_dish'),
    path('clear_order/<int:order_id>/clear/', views.clear_order, name='clear_order'),


    # Paypal URLs
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_cancel, name='payment_cancel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
