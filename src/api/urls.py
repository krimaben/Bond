from django.urls import path

from api.views import BuyBond, CreateBond, BondUsd, UpdateBond
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


urlpatterns = [
    # JWT Simple APIs URL
    path('login/', TokenObtainPairView.as_view(), name='user_login'),
    path('refesh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('varify_token/', TokenVerifyView.as_view(), name='token_varify'),

    # APIs URL
    path('api', CreateBond.as_view(), name='list_create_bonds'),
    path('api/<int:publication_id>/', BuyBond.as_view(), name='purchase_bond'),
    path('api/USD', BondUsd.as_view(), name='update_usd_rate'),
    path('api/update/<int:publication_id>/', UpdateBond.as_view(), name='update_bond'),
    path('api/delete/<int:publication_id>/', UpdateBond.as_view(), name='delete_bond')
]
