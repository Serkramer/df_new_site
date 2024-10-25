from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Prefetch, Sum, F, FloatField, ExpressionWrapper

from custom.models import Orders
from store.models import Materials, MaterialSheets, MaterialSheetStores
from web_project import TemplateLayout
from django.utils import timezone
from datetime import timedelta

# Create your views here.


# class MaterialInfoView(TemplateView):
#     # Predefined function
#     def get_context_data(self, **kwargs):
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))
#         materials = Materials.objects.filter(materialsheets__isnull=False).distinct()
#
#         sheets = MaterialSheets.objects.all()
#         sheet_stores = MaterialSheetStores.objects.filter(cell_branch_id=1)
#
#         today = timezone.now().date()
#         ninety_days_ago = today - timedelta(days=90)
#
#         orders = Orders.objects.filter(launch_date__range=(ninety_days_ago, today))
#
#         filtered_materials = []
#
#         for material in materials:
#             square = 0
#             material_sheets = sheets.filter(material=material)
#             material_count = []
#
#             orders_on_material = orders.filter(material_id=material.id)
#
#             orders_square = orders_on_material.aggregate(total_forms_area=Sum('forms_area'))['total_forms_area'] or 0
#
#             for sheet in material_sheets:
#                 # Calculate area for each sheet and multiply by count in storage
#                 sheet_counts = sheet_stores.filter(material_sheet=sheet)
#                 if sheet_counts.exists():
#                     material_count.extend(sheet_counts)
#
#                     for store in sheet_counts:
#                         # Calculate area of each piece and multiply by count
#                         if sheet.height and sheet.width:
#                             piece_area = sheet.height * sheet.width
#                             square += piece_area * (store.count or 0) / 1000000
#                 else:
#                     material_sheets = material_sheets.exclude(id=sheet.id)
#
#             material.material_sheets = material_sheets
#             material.material_count = material_count
#             material.square = round(square, 3)
#             material.orders_square = round(orders_square / 3, 3)
#             material.black_orders_square = round((float(orders_square) / 3) * 1.3, 3)
#             material.stock_months = round(float(material.square) / float(material.black_orders_square), 1) if material.black_orders_square > 0 else "---"
#             material.stock_days = round(material.stock_months * 30, 0) if material.black_orders_square > 0 else "---"
#             material.end_date = today + timedelta(days=material.stock_days) if material.black_orders_square > 0 else "---"
#
#             if material_count:
#                 filtered_materials.append(material)
#
#         context['materials'] = filtered_materials
#         return context


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
