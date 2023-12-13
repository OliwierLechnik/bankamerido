"""bankamerido URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from login.views import login_view, register_view, logout_view
from account.views import account_picker_view, account_create_view, account_detailed_view, all_accounts_view, accept_account_view
from book.views import regular_transfer_view, whole_history_view, debt_collection_view, debt_collection_group_view, money_withdraw_view, money_deposit_view, super_transfer_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view),
    path('register/', register_view),
    path('account/', account_picker_view),
    path('account/new/', account_create_view),
    path('account/<int:acc_id>/', account_detailed_view),
    path('account/<int:acc_id>/debt_collection/', debt_collection_view),
    path('account/<int:acc_id>/debt_collection_group/', debt_collection_group_view),
    path('account/<int:acc_id>/withdraw/', money_withdraw_view),
    path('account/<int:acc_id>/deposit/', money_deposit_view),
    path('account/<int:acc_id>/super_transfer/', super_transfer_view),
    path('account/all_accounts/', all_accounts_view),
    path('account/accept_account/', accept_account_view),
    path('account/<int:acc_id>/history/<int:page>', whole_history_view),
    path('account/<int:acc_id>/transfer/', regular_transfer_view),
    path('logout/', logout_view)
]
