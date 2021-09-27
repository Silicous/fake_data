from django.urls import path
from .views import LoginView, LogoutView, PageRedirect, MySchemasView, CreateSchemaView, DeleteSchemaView, \
    EditSchemaView, DataSetsView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', PageRedirect.as_view(), name='signup'),
    path('schemas/', MySchemasView.as_view(), name='list'),
    path("schemas/create", CreateSchemaView.as_view(), name="create"),
    path("schemas/edit/<int:pk>", EditSchemaView.as_view(), name="edit"),
    path("schemas/delete/<int:pk>", DeleteSchemaView.as_view(), name="delete"),
    path("schemas/export/<pk>", DataSetsView.as_view(), name="datasets"),
    path('accounts/', PageRedirect.as_view(), name='profile'),
    path('accounts/profile/', PageRedirect.as_view(), name='profile'),
]
