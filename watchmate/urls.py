
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # agregamos las urls de la app watchlist_app
    path('watch/', include('watchlist_app.api.urls')),
    # login temporary, esto es temporal
    # path('api-auth', include('rest_framework.urls')),
    # urls para login , logout , token authtentication
    path('account/', include('user_app.api.urls')),


]
