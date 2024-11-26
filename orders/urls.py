from django.contrib.auth.decorators import login_required
from django.urls import path

from orders.views import OrdersTableView, OrdersTableDataView, upload_files, GetOrderInfoView, delete_file

app_name = 'orders'

urlpatterns = [

    path('orders-table', login_required(OrdersTableView.as_view(template_name="orders/orders-table.html")), name="orders-table"),
    path('orders_data/', login_required(OrdersTableDataView.as_view()), name='orders_data'),
    path('upload_files/', upload_files, name='upload_files'),
    path('delete_file/', delete_file, name='delete_file'),
    path('get_order_info/', login_required(GetOrderInfoView.as_view()), name='get_order_info')

]
