from django.urls import path
from . import views

urlpatterns = [
    path('users/unblock', views.Reenable.as_view()),
    path('users/block', views.BlockUser.as_view()),
    path('users/<uuid:pk>/state', views.ChangeUserState.as_view()),
    path('users', views.UserList.as_view()),
    path('users/<uuid:pk>', views.UserDetail.as_view()),
    path('users/<uuid:pk>/new_role', views.ChangeUserRole.as_view()),
    path('users/<uuid:pk>/make_admin', views.UpgradeToAdminView.as_view()),
    path('users/<uuid:pk>/reset_password', views.ResetUserPassword.as_view()),
    path('roles', views.RolesList.as_view()),
]
