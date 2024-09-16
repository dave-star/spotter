from django.urls import path
from .views import Home

urlpatterns = [
    path ( 'books', Home.as_view ( ), name = 'books' ),
    path ( 'authors', Home.as_view ( ), name = 'authors' ),
    path ( 'books/<str:id>', Home.as_view ( ), name = 'books' ),
    path ( 'authors/<str:id>', Home.as_view ( ), name = 'authors' ),
    path ( 'favourites/<str:id>', Home.as_view ( ), name = 'favourites' ), # get a list fo favourites 
    path ( 'favourites/add', Home.as_view ( ), name = 'favourites_add' ),
    path ( 'favourites/remove/<str:id>', Home.as_view ( ), name = 'favourites_remove' ),
    path ( 'recommend', Home.as_view ( ), name = 'recommend' ),
]