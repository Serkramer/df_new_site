from django.contrib.auth.decorators import login_required
from django.urls import path

from orders.views import OrdersTableView, OrdersTableDataView

app_name = 'orders'

urlpatterns = [

    path('orders-table', login_required(OrdersTableView.as_view(template_name="orders/orders-table.html")), name="orders-table"),
    path('orders_data/', login_required(OrdersTableDataView.as_view()), name='orders_data'),

]
