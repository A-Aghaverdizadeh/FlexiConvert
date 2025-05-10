from django.conf.urls import handler404, handler403, handler400, handler500
from django.contrib.auth.decorators import login_required, permission_required
import rosetta.views as rosetta_views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from converter.sitemap import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('converter.urls')),
    path('rosetta/', include('rosetta.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('account/', include('useraccount.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'converter.views.page404'
handler403 = 'converter.views.page403'
handler400 = 'converter.views.page400'
handler500 = 'converter.views.page500'

# if settings.DEBUG or settings.ENABLE_ROSETTA:
#     urlpatterns += [
#         path(
#             'rosetta/',
#             login_required(permission_required('rosetta.can_translate')(include('rosetta.urls'))),
#         )
#     ]

