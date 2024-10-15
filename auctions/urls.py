from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path("categories/", views.categories_view, name="categories"),
    path("category/<int:category_id>", views.category_listings_view, name="category_listings"),
    path("list_detail/<int:list_id>", views.list_detail, name="list_detail"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/toggle/<int:list_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path('my_listings/', views.user_listings, name='user_listings'),
]
