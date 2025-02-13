from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('menu', views.menu , name='menu'),
    path('signup', views.signup, name='signup'),
    path('insertuser', views.insertuser, name='insertuser'),
    path('login', views.login, name='login'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('daily-activity/', views.daily_activity_create, name='daily_activity'),
    path('display-activity/', views.daily_activity_list_view, name='display_activity'),
    path('delete-activity/<int:id>', views.daily_activity_delete, name='delete_activity'),
    path('update-activity/<int:id>', views.daily_activity_update, name='update_activity'),
    path('add-goal/', views.goal_create, name='add_goal'),
    path('display-goals/', views.goals_list_view, name='display_goals'),
    path('update-goal/<int:id>', views.goal_update, name='update_goal'),
    path('delete-goal/<int:id>', views.goal_delete, name='delete_goal'),
    path('add-record/', views.journal_record_create, name='add_record'),
    path('display-records/', views.records_list_view, name='display_records'),
    path('update-record/<int:id>', views.record_update, name='update_record'),
    path('delete-record/<int:id>', views.record_delete, name='delete_record'),
    path('tips-tricks', views.tips_tricks, name='tips_tricks'),

]
