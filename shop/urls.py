from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # path('', views.main, name='main'),
    path('', views.Main.as_view(), name='main'),
    # path('gallery/', views.product_list, name='product_list'),
    path('tech_description/', views.Tech_description.as_view(), name='tech_description'),
    path('gallery/', views.ProdList.as_view(), name='product_list'),
    # path('gallery_work/', views.product_list_active, name='product_list_active'),
    path('gallery_work/', views.ProdListActive.as_view(), name='product_list_active'),
    # path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<slug:category_slug>/', views.ProdList.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    # path('<int:id>/<slug:slug>/', views.ProdDetail.as_view(), name='product_detail'),

]