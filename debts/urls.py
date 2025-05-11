# debts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Debtor CRUD
    path('',                              views.debtor_list,   name='debtor_list'),
    path('debtor/add/',                   views.debtor_add,    name='debtor_add'),
    path('debtor/<int:pk>/',              views.debtor_detail, name='debtor_detail'),
    path('debtor/<int:pk>/edit/',         views.debtor_edit,   name='debtor_edit'),
    path('debtor/<int:pk>/delete/',       views.debtor_delete, name='debtor_delete'),

    # Transaction CRUD (nested under debtor)
    path('debtor/<int:pk>/transaction/add/',             views.transaction_add,    name='transaction_add'),
    path('debtor/<int:debtor_pk>/transaction/<int:pk>/edit/',   views.transaction_edit,   name='transaction_edit'),
    path('debtor/<int:debtor_pk>/transaction/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
]
