from aiohttp.payload import Order
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from custom.models import Orders, OrderStatusList, OrderPlaneSlices, OrderFartuks
from web_project import TemplateLayout


# Create your views here.


class OrdersTableView(TemplateView):
    template_name = "your_template.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        orders = Orders.objects.all().order_by('-id')
        paginator = Paginator(orders, 100)  # 100 элементов на странице
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        for order in page_obj.object_list:
            order.fartuks = OrderFartuks.objects.filter(order=order)
            order.slices_count = OrderPlaneSlices.objects.filter(order=order).count()

        context['page_obj'] = page_obj  # Объект страницы для отображения в шаблоне
        context['orders'] = page_obj.object_list  # Текущая страница записей
        context['is_paginated'] = page_obj.has_other_pages()  # Проверка, нужна ли пагинация
        return context


class OrdersTableDataView(View):
    def get(self, request, *args, **kwargs):
        orders = Orders.objects.all().order_by('id')
        paginator = Paginator(orders, 100)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        data = {
            'orders': [
                {
                    'id': order.id,
                    'name': order.name,
                    'email': order.name,
                    'start_date': order.launch_date.strftime('%d.%m.%Y'),
                    'salary': order.name,
                    'status': order.get_status_display(),
                    'client':  order.company_client.id.name if order.company_client else None,
                    'printing_company': order.printing_company.id.name if order.printing_company else None

                } for order in page_obj.object_list
            ],
            'page': page_obj.number,
            'pages': paginator.num_pages
        }
        return JsonResponse(data)
