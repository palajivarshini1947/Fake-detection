"""
URL configuration for Fake Job Detection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FakeJobDetectionapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('menu/',views.menu,name='menu'),
    path('blog/',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),

    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('admin_index/',views.admin_index,name='admin_index'),
    path('admin_addnotification/',views.admin_addnotification,name='admin_addnotification'),
    path('admin_viewnotification/',views.admin_viewnotification,name='admin_viewnotification'),
    path('delete_notification/<int:id>',views.delete_notification,name='delete_notification'),
    path('admin_viewcontact/',views.admin_viewcontact,name='admin_viewcontact'),
    path('admin_viewcustomer/',views.admin_viewcustomer,name='admin_viewcustomer'),
    path('accept_customer/<int:id>/',views.accept_customer,name='accept_customer'),
    path('reject_customer/<int:id>/',views.reject_customer,name='reject_customer'),
    path('admin_password/',views.admin_password,name='admin_password'),
    path('admin_viewjobprovider/',views.admin_viewjobprovider,name='admin_viewjobprovider'),
    path('accept_jobprovider/<int:id>/',views.accept_jobprovider,name='accept_jobprovider'),
    path('reject_jobprovider/<int:id>/', views.reject_jobprovider, name='reject_jobprovider'),

    path('customer_index/',views.customer_index,name='customer_index'),
    path('customer_login/',views.customer_login,name='customer_login'),
    path('customer_otp_verify/',views.customer_otp_verify,name='customer_otp_verify'),
    path('customer_regi/',views.customer_regi,name='customer_regi'),
    path('customer_viewnotification/',views.customer_viewnotification,name='customer_viewnotification'),
    path('customer_changepassword/',views.customer_changepassword,name='customer_changepassword'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_otp_verify/', views.forgot_otp_verify, name='forgot_otp_verify'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('customer_profile/',views.customer_profile,name='customer_profile'),
    path('customer_editprofile/',views.customer_editprofile,name='customer_editprofile'),
    path('customer_viewjobs/',views.customer_viewjobs,name='customer_viewjobs'),
    path('customer_jobdetails/<int:id>/', views.customer_jobdetails, name='customer_jobdetails'),
    path('customer-apply-job/<int:id>/', views.customer_apply_job, name='customer_apply_job'),
    path('customer-my-applications/', views.customer_my_applications, name='customer_my_applications'),

    path('fake-job-detector/', views.fake_job_detector, name='fake_job_detector'),
    path('predict-job/', views.predict_job, name='predict_job'),
    path('jobprovider_login/',views.jobprovider_login,name='jobprovider_login'),
    path('jobprovider_regi/',views.jobprovider_regi,name='jobprovider_regi'),
    path('jobprovider_index/',views.jobprovider_index,name='jobprovider_index'),
    path('jobprovider_otp_verify/',views.jobprovider_otp_verify,name='jobprovider_otp_verify'),
    path('jobprovider_profile/',views.jobprovider_profile,name='jobprovider_profile'),
    path('jobprovider_editprofile/', views.jobprovider_editprofile, name='jobprovider_editprofile'),
    path('jobprovider_changepassword/', views.jobprovider_changepassword, name='jobprovider_changepassword'),
    path('jobprovider_viewnotification/', views.jobprovider_viewnotification, name='jobprovider_viewnotification'),
    path('jobprovider_addjob/', views.jobprovider_addjob, name='jobprovider_addjob'),
    path('jobprovider_viewjobs/', views.jobprovider_viewjobs, name='jobprovider_viewjobs'),
    path('jobprovider-jobdetails/<int:id>/', views.jobprovider_jobdetails, name='jobprovider_jobdetails'),
    path('jobprovider_viewapplication/<int:job_id>/',views.jobprovider_viewapplication, name='jobprovider_viewapplication'),
    path('jobprovider-accept-application/<int:app_id>/', views.jobprovider_accept_application, name='jobprovider_accept_application'),
    path('jobprovider-reject-application/<int:app_id>/', views.jobprovider_reject_application, name='jobprovider_reject_application'),
    path('jobprovider_editjobs/<int:id>/', views.jobprovider_editjobs, name='jobprovider_editjobs'),
    path('jobprovider-deletejob/<int:id>/', views.jobprovider_deletejob, name='jobprovider_deletejob'),
    path('jobprovider_forgot_password/', views.jobprovider_forgot_password, name='jobprovider_forgot_password'),
    path('jobprovider_forgot_otp_verify/',views.jobprovider_forgot_otp_verify,name='jobprovider_forgot_otp_verify'),
    path('jobprovider_reset_password/', views.jobprovider_reset_password, name='jobprovider_reset_password'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)