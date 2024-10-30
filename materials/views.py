import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Prefetch, Sum, F, FloatField, ExpressionWrapper, Count
from collections import defaultdict
from custom.models import Orders, OrderStatusList
from materials.forms import MaterialChartsForm
from store.models import Materials, MaterialSheets, MaterialSheetStores
from web_project import TemplateLayout
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.db.models.functions import TruncMonth, ExtractWeek, Extract, TruncWeek, TruncDay


class MaterialInfoView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        today = timezone.now().date()
        ninety_days_ago = today - timedelta(days=90)

        # Prefetch related fields to reduce database hits
        materials = (
            Materials.objects.filter(materialsheets__isnull=False)
            .distinct()
            .prefetch_related(
                Prefetch(
                    'materialsheets_set',  # use the default reverse lookup name
                    queryset=MaterialSheets.objects.annotate(
                        area=F('height') * F('width') / 1000000
                    ),
                    to_attr='sheets'
                )
            )
        )

        # Aggregate count of sheets in store for each material and pre-calculate total sheet area in stock
        sheet_stores = (
            MaterialSheetStores.objects
            .filter(cell_branch_id=1)
            .annotate(
                area=ExpressionWrapper(
                    F('material_sheet__height') * F('material_sheet__width') / 1000000,
                    output_field=FloatField()
                )
            )
            .values('material_sheet__material_id')
            .annotate(
                total_area_in_stock=Sum(F('count') * F('area'))
            )
        )

        orders = (
            Orders.objects.filter(launch_date__range=(ninety_days_ago, today))
            .values('material_id')
            .annotate(total_forms_area=Sum('forms_area'))
        )

        # Получаем данные о количестве листов по каждому размеру для каждого материала
        sheet_counts_by_size = (
            MaterialSheetStores.objects
            .filter(cell_branch_id=1)
            .values('material_sheet__material_id', 'material_sheet__height', 'material_sheet__width')
            .annotate(total_count=Sum('count'))
        )

        # Преобразуем данные в словарь по material_id для быстрого доступа
        sheet_count_by_size_dict = {}
        for item in sheet_counts_by_size:
            material_id = item['material_sheet__material_id']
            height = item['material_sheet__height']
            width = item['material_sheet__width']
            count = item['total_count']

            if material_id not in sheet_count_by_size_dict:
                sheet_count_by_size_dict[material_id] = []

            # Добавляем запись о размере и количестве
            sheet_count_by_size_dict[material_id].append({
                'height': height,
                'width': width,
                'count': count,
            })

        # Build filtered materials list with annotations and calculated fields
        filtered_materials = []
        for material in materials:
            # Получаем информацию о листах по каждому размеру
            sheets_info = sheet_count_by_size_dict.get(material.id, [])

            sheet_area_in_stock = next(
                (store['total_area_in_stock'] for store in sheet_stores if
                 store['material_sheet__material_id'] == material.id),
                0
            )

            orders_square = next(
                (order['total_forms_area'] for order in orders if order['material_id'] == material.id),
                0
            )

            # Calculated fields
            material.square = round(sheet_area_in_stock, 3)
            material.orders_square = round(float(orders_square) / 3, 3) if orders_square else 0
            material.black_orders_square = round(float(material.orders_square * 1.3), 3)
            material.stock_months = (
                round(material.square / material.black_orders_square, 1)
                if material.black_orders_square > 0 else "---"
            )
            material.stock_days = (
                round(material.stock_months * 30, 0)
                if material.black_orders_square > 0 else "---"
            )
            material.end_date = (
                today + timedelta(days=material.stock_days)
                if material.black_orders_square > 0 else "---"
            )

            # Сохраняем информацию о листах с количеством
            material.sheets_info = sheets_info

            if sheet_area_in_stock > 0:
                filtered_materials.append(material)

        context['materials'] = filtered_materials
        return context


class MaterialsChartsView(TemplateView):
    template_name = "materials/materials_charts.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = kwargs.get('form', MaterialChartsForm())
        context['form'] = kwargs.get('form', MaterialChartsForm())

        # Собираем данные материалов для передачи в шаблон
        context['materials_data'] = form

        return context

    def post(self, request, *args, **kwargs):
        form = MaterialChartsForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            thickness = form.cleaned_data['thickness']
            materials = form.cleaned_data['materials']

            start_datetime = datetime.combine(start_date, time.min)
            end_datetime = datetime.combine(end_date, time.max)

            not_use_status_list = [OrderStatusList.NONE, OrderStatusList.ERROR_FILE_COUNT, OrderStatusList.CANCEL,
                                   OrderStatusList.STOP_BY_CLIENT, OrderStatusList.STOP]

            orders = Orders.objects.filter(launch_date__gte=start_datetime, launch_date__lte=end_datetime).exclude(
                status__in=not_use_status_list).exclude(launch_date__isnull=True)

            if thickness:
                material_ids = list(Materials.objects.using('store').filter(thickness__in=thickness).values_list('id',
                                                                                                            flat=True))
                orders = orders.filter(material_id__in=material_ids)

            if materials:
                material_ids = list(materials.values_list('id', flat=True))
                orders = orders.filter(material_id__in=material_ids)

            area_sum_by_month = (
                orders
                .annotate(month=TruncMonth('launch_date'))
                .values('month')
                .annotate(total_area=Sum('forms_area'))
                .order_by('month')
            )

            orders_in_month = [
                {
                    'month': f"{month_data['month'].strftime('%m')}.{month_data['month'].year}",
                    'total_area': month_data['total_area'],
                    'total_area_int': int(month_data['total_area'] or 0)
                }
                for month_data in area_sum_by_month
            ]

            max_in_month = int(round(max((item['total_area'] for item in orders_in_month), default=0), -2))

            area_sum_by_week = (
                orders
                .annotate(week=TruncWeek('launch_date'))
                .values('week')
                .annotate(total_area=Sum('forms_area'))
                .order_by('week')
            )

            orders_in_week = [
                {
                    'week': f"{week_data['week'].isocalendar()[1]:02d}.{week_data['week'].year}",
                    'total_area': week_data['total_area'],
                    'total_area_int': int(week_data['total_area'] or 0)
                }
                for week_data in area_sum_by_week
            ]

            max_in_week = int(round(max((item['total_area'] for item in orders_in_week), default=0), -2))

            area_sum_by_day = (
                orders
                .annotate(day=TruncDay('launch_date'))
                .values('day')
                .annotate(total_area=Sum('forms_area'))
                .order_by('day')
            )

            orders_in_day = [
                {
                    'day': day_data['day'].strftime('%d.%m.%Y'),
                    'total_area': day_data['total_area'],
                    'total_area_int': int(day_data['total_area'] or 0)
                }
                for day_data in area_sum_by_day
            ]
            max_in_day = int(round(max((item['total_area'] for item in orders_in_day), default=0), -2))

            # Фильтрация по компаниям и выборка нужных полей
            orders_by_company = (
                orders
                .values('company_client__id', 'company_client__id__name')  # Группировка по id и названию компании
                .annotate(total_forms_area=Sum('forms_area'))
                .order_by('-total_forms_area')
            )

            # Преобразование данных для вывода
            orders_with_area_company = [
                {
                    'company_name': order['company_client__id__name'],
                    'forms_area': order['total_forms_area'],
                    'forms_area_int': int(order['total_forms_area'] or 0)
                }
                for order in orders_by_company
            ]

            # Пример максимального значения для forms_area по выбранной компании
            max_forms_area_company = int(round(max((item['forms_area'] for item in orders_with_area_company),
                                                   default=0), -2))

            company_count = len(orders_with_area_company)
            height = company_count * 20 if company_count else 400
            return self.render_to_response(self.get_context_data(form=form, orders_in_month=orders_in_month,
                                                                 max_in_month=max_in_month, show_modal=True,
                                                                 orders_in_week=orders_in_week,
                                                                 max_in_week=max_in_week,
                                                                 orders_in_day=orders_in_day,
                                                                 max_in_day=max_in_day,
                                                                 max_forms_area_company=max_forms_area_company,
                                                                 orders_with_area_company=orders_with_area_company,
                                                                 company_count=company_count, height=height))

        else:
            # Если форма не прошла валидацию
            return self.render_to_response(self.get_context_data(form=form))




