from django.urls import path
from . import views
from . import url_handlers

urlpatterns = [
    path("pojistenec_index/", views.PojistenecIndex.as_view(), name="pojistenec_index"),
    path("pojisteni_index/", views.PojisteniIndex.as_view(), name="pojisteni_index"),
    path("<int:pk>/pojistenec_detail/", views.DetailPojistenceView.as_view(), name="pojistenec_detail"),
    path("<int:pk>/pojisteni_detail/", views.DetailPojisteniView.as_view(), name="pojisteni_detail"),
    path("vytvor_pojistence/", views.VytvorPojistence.as_view(), name="novy_pojistenec"),
    path("vytvor_pojisteni/", views.VytvorPojisteni.as_view(), name="nove_pojisteni"),
    path("home/", views.Home.as_view(), name="home"),
    path("", url_handlers.index_handler),
    path("register/", views.UzivatelViewRegister.as_view(), name="registrace"),
    path("login/", views.UzivatelViewLogin.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("<int:pk>/edit/", views.EditPojistenec.as_view(), name="edit_pojistenec"),
]
