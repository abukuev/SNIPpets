from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name = "home"),
    path('snippets/add', views.add_snippet_page, name = "add_sn"),
    path('snippets/list', views.snippets_page, name = "view_sn"),
    path('snippets/<int:snippetid>', views.snippet_view, name = "get_sn"),
    path('snippets/<int:snippetid>/edit', views.snippets_edit, name = "edit_sn"),
    path('snippets/<int:snippetid>/del', views.snippets_del, name = "del_sn"),
    path('login', views.login, name = "login"),
    path('logout', views.logout, name = "logout"),
    path('snippets/my', views.snippets_my, name = "my_sn"),
    path('registration', views.create_user, name = "register"),
    path('comment/add', views.comment_add, name="comment_add")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
