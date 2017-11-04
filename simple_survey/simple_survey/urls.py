from django.conf.urls import url, include

from django.contrib import admin
from survey import urls as appurls
admin.autodiscover()

urlpatterns = (
    # Examples:
    # url(r'^$', 'simple_survey.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^',include(appurls)),
    url(r'^admin/', include(admin.site.urls)),
)
