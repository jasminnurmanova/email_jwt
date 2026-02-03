from django.urls import path
from .views import SignUpView, LoginView, ProfileView,ProfileUpdateView, \
    LogoutView,ChangePasswordView,CartView,CartUpdateView,CartAddView,CartRemoveView,CartClearView,OrderCancelView,OrderCreateView,OrderDetailView,OrderListView


urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile-update/', ProfileUpdateView.as_view()),
    # path('code/', Test.as_view()),
    path('change-password/', ChangePasswordView.as_view(),),
    path('card/', CartView.as_view(),),
    path('add/', CartAddView.as_view(),),
    path('delete/', CartRemoveView.as_view(),),
    path('update/', CartUpdateView.as_view(),),
    path('clear/', CartClearView.as_view(),),
    path('create/', OrderCreateView.as_view()),
    path('list/', OrderListView.as_view()),
    path('detail/<int:pk>/', OrderDetailView.as_view()),
    path('cancel/<int:pk>/', OrderCancelView.as_view()),

]