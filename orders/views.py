from aiohttp.payload import Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db.models import Q
from custom.models import Orders, OrderStatusList, OrderPlaneSlices, OrderFartuks, OrderDampers
from orders.forms import OrderViewForm, OrderFartuksForm, PlaneSliceForm, OrderDeliveryViewForm
from orders.models import FilesAllowedExtensions
from web_project import TemplateLayout
import os
import time
import paramiko
from django.conf import settings
from django.core.serializers import serialize

# Create your views here.
from .serializers import (
    OrdersSerializer,
    OrderDampersSerializer,
    OrderFartuksSerializer,
    OrderPlaneSlicesSerializer,
)


class OrdersTableView(TemplateView):
    template_name = "orders/orders-table.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        create_order_form = OrderViewForm()
        all_extensions = FilesAllowedExtensions.objects.values_list('extension', flat=True)
        context['allowed_extensions'] = list(all_extensions)
        context['create_order_form'] = create_order_form
        context['order_fartuks_form'] = OrderFartuksForm()
        context['order_plane_slice_form'] = PlaneSliceForm()
        context['delivery_form'] = OrderDeliveryViewForm()
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
                'shipping_date_planed': order.order_delivery.shipping_date_planed.strftime(
                    '%d.%m.%Y %H:%M') if order.order_delivery and order.order_delivery.shipping_date_planed else None,
                'shipping_date_departure': order.order_delivery.shipping_date_departure.strftime(
                    '%d.%m.%Y %H:%M') if order.order_delivery and order.order_delivery.shipping_date_departure else None,
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


class GetOrderInfoView(View):

    def get(self, request, *args, **kwargs):
        order_id = int(request.GET.get('order_id', -1))

        if order_id == -1:
            return JsonResponse({'status': 'error', 'message': 'Не удалось считать номер заказа'})

        user = request.user
        if not (user.is_authenticated and user.is_active and user.is_staff):
            return JsonResponse({'status': 'error', 'message': 'У вас нет прав для просмотра информации'})

        editable = user.groups.filter(name="Репрограф").exists()

        order = Orders.objects.filter(pk=order_id).first()
        if not order:
            return JsonResponse({'status': 'error', 'message': 'Заказ не найден'})

        # Сериализация объектов
        order_data = OrdersSerializer(order).data
        dampers_data = OrderDampersSerializer(OrderDampers.objects.filter(order=order), many=True).data
        fartuks_data = OrderFartuksSerializer(OrderFartuks.objects.filter(order=order), many=True).data
        slices_data = OrderPlaneSlicesSerializer(OrderPlaneSlices.objects.filter(order=order), many=True).data

        return JsonResponse({
            'status': 'success',
            'order': order_data,
            'dampers': dampers_data,
            'fartuks': fartuks_data,
            'slices': slices_data,
            'editable': editable,
        })


def load_work_files(self, request):
    pass


@csrf_exempt
@login_required
def upload_files(request):
    if request.method == 'POST' and request.FILES:
        username = request.user.username
        timestamp = int(time.time())
        temp_dir = f"{username}/{timestamp}"

        # Создаем временную папку на SFTP
        remote_dir = os.path.join(settings.UPLOAD_FOLDER, temp_dir)

        try:
            # Подключение к SFTP
            transport = paramiko.Transport((settings.HOST, settings.PORT))
            transport.connect(username=settings.FTP_LOGIN, password=settings.FTP_PASS)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Создаем папку для загрузки, если она еще не создана
            try:
                sftp.stat(remote_dir)
            except FileNotFoundError:
                sftp.mkdir(remote_dir)

            # Загружаем файл на SFTP
            uploaded_file = next(request.FILES.values())
            remote_path = os.path.join(remote_dir, uploaded_file.name)
            with sftp.file(remote_path, 'wb') as sftp_file:
                sftp_file.write(uploaded_file.read())

            sftp.close()
            transport.close()
            return JsonResponse({"message": "Файл успешно загружен на FTP!"})

        except Exception as e:
            return JsonResponse({"error": f"Ошибка загрузки файла: {str(e)}"}, status=500)

    return JsonResponse({"error": "Ошибка загрузки файла"}, status=400)
