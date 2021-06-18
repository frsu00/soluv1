from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.HomePageView.as_view(), name='home'),
    path('', views.home, name='home'),
    path('productos', views.ProductListView, name='product-list'),
    path('productos/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('registro/', views.RegistrationView.as_view(), name='register'),
    path('add_to_cart/<int:product_pk>', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_cart/<int:product_pk>', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('carrito/', views.PedidoDetailView.as_view(), name='pedido-detail'),
    path('checkout/<int:pk>', views.PedidoUpdateView.as_view(), name='pedido-update'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('complete_payment/', views.CompletePaymentView.as_view(), name='complete-payment'),

    path('addproduct/', views.createProduct, name='addproduct'),
    path('editproduct/<str:pk>', views.editProduct, name='editproduct'),
    path('allmyproducts/', views.seeProduct, name='allmyproducts'),
    path('deleteproduct/<str:pk>', views.deleteProduct, name='deleteproduct'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)