from rest_framework.routers import DefaultRouter

from api.products.views import ProductsViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
urlpatterns = router.urls
