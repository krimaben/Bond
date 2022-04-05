from django.urls import path

from api.views import BuyBond, CreateBond, BondUsd, UpdateBond
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api", CreateBond.as_view()),
    path("api/<int:publication_id>/", BuyBond.as_view()),
    path("api/USD", BondUsd.as_view()),
    path("api/update/<int:publication_id>/", UpdateBond.as_view()),
    path("api/delete/<int:publication_id>/", UpdateBond.as_view()),
]
