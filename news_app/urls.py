from django.urls import path
from .views import news_list, news_detail, HomePageView, contactsPageView, \
    LocalNewsView, ForeignNewsView, TechnologyNewsView, SportNewsView, ErrorPageView

urlpatterns = [
    path('', HomePageView.as_view(), name="home_view"),
    path('contacts/', contactsPageView.as_view(), name="contacts_view"),
    path("all/", news_list, name="all_news_list"),
    path("404/", ErrorPageView.as_view(), name='error_view'),
    path("technology/", TechnologyNewsView.as_view(), name="technology_news_page"),
    path('local/', LocalNewsView.as_view(), name="local_news_page"),
    path("foreign/", ForeignNewsView.as_view(), name='foreign_news_page'),
    path("sport/", SportNewsView.as_view(), name="sport_news_page"),
    path('<slug:news>/', news_detail, name="news_detail_page"),
]
