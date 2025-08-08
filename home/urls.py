from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("logout/", views.view_logout, name="logout"),
    path("home/", views.home, name="home"),
    # users
    path("list_user/", views.list_user, name="list_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/<int:id_user>/", views.update_user, name="upadate_user"),
    path("delete_user/<int:id_user>/", views.delete_user, name="delete_user"),
    path("alter_password/<int:id_user>/", views.alter_password, name="alter_password"),
    path("register_client/<int:id_event>/", views.register_client, name="register_client"),
    # events
    path("deteils_event/<int:id_event>/", views.deteils_event, name="deteils_event"),
    path("buy_ticket/<int:id_event>/", views.buy_ticket, name="buy_ticket"),
    path("register_events/", views.register_event, name="register_event"),
    path("update_event/<int:id_event>/", views.update_event, name="update_event"),
    path("delete_event/<int:id_event>/", views.delete_event, name="delete_event"),
    path("tickets/<int:id_event>/", views.tickets_generate, name="tickets"),
    path("ticket/<str:ticket_id>/export-pdf", views.export_ticket_pdf, name="export_ticket_pdf"),
    # setores
    path("list_setor/<int:id_event>/", views.list_setor, name="list_setores"),
    path("register_setor/<int:event_id>/", views.register_setor, name="register_setor"),
    path("update_setor/<int:id_setor>/", views.update_setor, name="update_setor"),
    path("delete_setor/<int:id_setor>/", views.delete_setor, name="delete_setor")
]
