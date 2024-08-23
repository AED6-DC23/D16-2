from django.urls import path, include
from . import views
from .views import PostDetailView, PostList, PostCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', views.index),
    path('main', views.base),    
    path('about-us', views.about),
    path('contacts', views.contacts),
    path('mynews', views.mynews),
    path('news', views.news),
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('account/', include('account.urls')),
    
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    #path('subscriptions/', subscriptions, name='subscriptions'),
]



