from rest_framework import routers

from .views import (
    UserRegistrationLoginViewSet,
    ProductViewSet,
    BillViewSet,
    BillDetailViewSet,
)

router = routers.SimpleRouter()
router.register(r"auth", UserRegistrationLoginViewSet, basename="auth")
router.register(r"products", ProductViewSet)
router.register(r"bills", BillViewSet)
router.register(r"bill-details", BillDetailViewSet, basename="customer-bill-details")

urlpatterns = router.urls + []
