
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # agregamos las urls de la app watchlist_app
    path('watch/', include('watchlist_app.api.urls'))
]
