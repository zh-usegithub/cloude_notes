from django.urls import path
from . import views
urlpatterns = [
    path('add_notes/', views.add_notes),
    path('del_notes/<int:id>',views.del_notes),
    path('del_allnotes/<int:user_id>/',views.del_all_notes),
    path('del_allnotes/',views.del_all_notes)
]