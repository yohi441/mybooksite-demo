
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "BOOKSITE Admin"
admin.site.site_title = "BOOKSITE Admin Portal"
admin.site.index_title = "Welcome to BOOKSITE Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("mybooksite.urls")),
    path('accounts/', include("accounts.urls")),
    path('carts/', include("carts.urls")),
    # path('accounts/', include("django.contrib.auth.urls")),
] 


