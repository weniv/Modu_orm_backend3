from django.urls import path
from .views import accounts_details

"""
www.hojun.com/accounts/hojun # accounts > accounts_details (유저 상세)
www.hojun.com/accounts/junho
"""

urlpatterns = [
    path("<str:username>/", accounts_details),
]
