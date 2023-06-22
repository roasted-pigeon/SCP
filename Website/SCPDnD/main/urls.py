from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mainPage, name='main'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('audio', views.showAudio, name='audioLibrary'),
    path('audio/upload', views.uploadAudio, name='audioUpload'),
    path('images', views.showImages, name='imageLibrary'),
    path('images/upload', views.uploadImage, name='imageUpload'),
    path('account', views.account, name='account'),
    path('documents', views.showDocuments, name='documentLibrary'),
    path('documents/upload', views.uploadDocument, name='documentUpload'),
    path('games', views.showGames, name='gameLibrary'),
    path('games/create', views.createGame, name='gameCreate'),
    path('createGameScreen', views.tableGenerator, name='gameScreenCreate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
