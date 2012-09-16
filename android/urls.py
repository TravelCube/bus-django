from django.conf.urls import patterns, include, url

urlpatterns = patterns('android.views',
            url(r'^lines/', 'lines'),
            url(r'^stops/', 'stops'),
            url(r'^log/userop*', 'userop'),
            )

