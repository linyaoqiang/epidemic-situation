import admin.urls as admin_urls
import user.urls as user_urls
urlpatterns = [
    *admin_urls.urlpatterns,
    *user_urls.urlpatterns
]
