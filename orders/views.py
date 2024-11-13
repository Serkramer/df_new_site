from aiohttp.payload import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db.models import Q
from custom.models import Orders, OrderStatusList, OrderPlaneSlices, OrderFartuks
from orders.models import FilesAllowedExtensions
from web_project import TemplateLayout
import os
import time
import paramiko
from django.conf import settings
# Create your views here.


class OrdersTableView(TemplateView):
    template_name = "orders/orders-table.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        all_extensions = FilesAllowedExtensions.objects.values_list('extension', flat=True)
        context['allowed_extensions'] = list(all_extensions)
        return context


class OrdersTableDataView(View):
    def get(self, request, *args, **kwargs):

        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '').strip()

        orders_queryset = Orders.objects.all().order_by('-id')

        # Фильтрация при наличии поискового запроса
        if search_value:
            orders_queryset = orders_queryset.filter(
               Q(name__icontains=search_value)  # |
                # Q(email__icontains=search_value) |
                # Q(city__icontains=search_value) |
                # Q(post__icontains=search_value) |
                # Q(status__icontains=search_value)
            )

        # Общее количество записей
        records_total = Orders.objects.count()
        # Количество записей после фильтрации
        records_filtered = orders_queryset.count()
        # Применение пагинации
        orders = orders_queryset[start:start + length]

        for order in orders:
            order.fartuks = OrderFartuks.objects.filter(order=order)
            order.slices_count = OrderPlaneSlices.objects.filter(order=order)

        data = [
            {
                'id': order.id,
                'start_date': order.launch_date.strftime('%d.%m.%Y'),
                'status': order.get_status_display(),
                'client': order.company_client.id.name if order.company_client else None,
                'printing_company': order.printing_company.id.name if order.printing_company else None,
                'name': order.name,
                'technology': order.cliche_technology.name if order.cliche_technology else None,
                'order_material': None,
                'ruling': None,
                'slices_count': order.slices_count.count(),
                'forms_area': order.forms_area,
                'fartuks_area': order.fartuks_area,
                'fartuk': order.fartuk.type if order.fartuk else None,
                'fartuks': None,
                'pay': None,
                'check': None,
                'shipping_date_planed': order.order_delivery.shipping_date_planed.strftime('%d.%m.%Y %H:%M') if order.order_delivery and order.order_delivery.shipping_date_planed else None,
                'shipping_date_departure': order.order_delivery.shipping_date_departure.strftime('%d.%m.%Y %H:%M') if order.order_delivery and order.order_delivery.shipping_date_departure else None,
                'delivery': None,
                'contact': None,
                # 'is_defective':  order.is_defective if order.is_defective else False


            } for order in orders
        ]

        response = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data
        }
        return JsonResponse(response)


def load_work_files(self, request):
    pass


@login_required
def upload_files(request):
    if request.method == 'POST' and request.FILES:
        username = request.user.username
        timestamp = int(time.time())
        temp_dir = f"{username}_{timestamp}"

        # Создаем временную папку на SFTP
        transport = paramiko.Transport((settings.HOST, settings.PORT))
        transport.connect(username=settings.FTP_LOGIN, password=settings.FTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_dir = os.path.join(settings.UPLOAD_FOLDER, temp_dir)
        sftp.mkdir(remote_dir)

        # Сохраняем каждый файл в созданной временной папке
        for file_key, file in request.FILES.items():
            remote_path = os.path.join(remote_dir, file.name)
            with sftp.file(remote_path, 'wb') as sftp_file:
                sftp_file.write(file.read())

        sftp.close()
        transport.close()

        return JsonResponse({"message": "Файлы успешно загружены в временную папку!"})
    return JsonResponse({"error": "Ошибка загрузки файлов"}, status=400)
