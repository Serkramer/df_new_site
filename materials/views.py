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
from django.db.models.functions import TruncMonth


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
        context['form'] = kwargs.get('form', MaterialChartsForm())
        return context

    def post(self, request, *args, **kwargs):
        form = MaterialChartsForm(request.POST)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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
                status__in=not_use_status_list)

            if thickness:
                # orders = orders.filter()
                pass

            if materials:
                material_ids = list(materials.values_list('id', flat=True))
                orders = orders.filter(material_id__in=material_ids)

            area_sum_by_month = defaultdict(lambda: 0)

            for order in orders:
                launch_date = timezone.localtime(order.launch_date)
                # Извлекаем месяц и год из даты
                month = launch_date.strftime('%m/%Y')
                if order.forms_area:
                    area_sum_by_month[month] += order.forms_area

            orders_in_month = [{'month': month, 'total_area': total_area, 'total_area_int': int(total_area)} for
                               month, total_area in
                               sorted(area_sum_by_month.items())]

            max_in_month = int(round(max((item['total_area'] for item in orders_in_month), default=0), -2))

            return self.render_to_response(self.get_context_data(form=form, orders_in_month=orders_in_month,
                                                                 max_in_month=max_in_month, show_modal=True))

        else:
            # Если форма не прошла валидацию
            return self.render_to_response(self.get_context_data(form=form))
