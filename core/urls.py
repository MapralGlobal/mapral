from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact,name="contact"),
    path('blog/',views.blog,name="blog"),
    path('services/',views.services,name="services"),
    path('blogItem/<str:slug>',views.blogItem,name="blogItem"),
    path('login/',views.loginView,name="login"),
    path('signup/',views.signView,name="signView"),
    path('rbuilder/',views.rbuilder,name="rbuilder"),
    path('resume/',views.resumeList,name="resume"),
    path('resumeView/<int:id>',views.resume,name="resume"),
    path('resumeDelete/<int:id>',views.resumeDelete,name="resume"),
    path('jobUpdate/',views.jobUpdate,name="jobUpdate"),
    path('jobUpdate/update',views.jobUpdate1,name="jobUpdate1"),
    path('logout/',views.logoutView,name="logout"),
    path('verifyEmail/<str:token>',views.verifyEmail,name="verifyEmail"),
    path('dashboard/',views.dashboard,name="dashboard"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
