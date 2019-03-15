from django.urls import path, include
from django.conf import settings
from . import views
from django.views.static import serve

urlpatterns = [
    path('', views.index, name='index'),
    path('viewPost/<int:post_id>/', views.viewPost, name='viewPost'),
    path('addPost/', views.addPost, name='addPost'),
    path('addItem/<int:item_id>/', views.addItem, name='addItem'),
    path('deletePost/<int:post_id>/', views.deletePost, name='deletePost'),
    path('deleteItem/<int:item_id>/', views.deleteItem, name='deleteItem'),
    path('editPost/<int:post_id>/', views.editPost, name='editPost'),
    path('editItem/<int:item_id>/', views.editItem, name='editItem'),
    path('listPost/', views.listPost, name='listPost'),
    path('newUser/', views.newUser, name='newUser'),
    path('postDetails/', views.postDetails, name='postDetails'),
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
