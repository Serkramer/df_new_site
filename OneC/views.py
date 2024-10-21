from aiohttp.payload import Order
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json
from OneC.functions import get_exchange_rate
from OneC.models import Price, CompanyWithNuances, Check
from custom.models import CompanyClients, Orders, CompanyOurBrands
from web_project import TemplateLayout
import datetime

class CheckView(TemplateView):
    template_name = "OneC/check_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exchange_rate'] = get_exchange_rate()
        return context


class CheckListView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


class CreateCheckView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['clients'] = CompanyClients.objects.filter(id__is_verified=True).exclude(id__is_outdated=True)
        context['our_companies'] = CompanyOurBrands.objects.all()

        return context


@login_required
@csrf_exempt
def get_orders_from_clients_and_dates(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        company_id = int(body_data.get('company_id'))
        start_day = body_data.get('start_day')
        end_day = body_data.get('end_day')

        if company_id and start_day and end_day:
            client_company = CompanyClients.objects.filter(id__id=company_id).first()
            start_date = datetime.datetime.strptime(start_day, '%m/%d/%Y')
            end_date = datetime.datetime.strptime(end_day, '%m/%d/%Y')
            end_date = end_date.replace(hour=23, minute=59, second=59)

            orders = Orders.objects.filter(company_client__id__id=company_id, launch_date__gte=start_date,
                                           launch_date__lte=end_date)
            company_our_brand = -1
            if client_company.company_our_brand:
                our_company = CompanyOurBrands.objects.filter(id__id=client_company.company_our_brand.id.id).first()
                company_our_brand = our_company.id.id
            orders_list = list(orders.values('id', 'name'))

            return JsonResponse({'orders': orders_list, 'company_our_brand': company_our_brand})

        return JsonResponse({'error': 'Invalid request'})


@login_required
@csrf_exempt
def generate_check(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        company_id = int(body_data.get('company_id'))
        start_day = body_data.get('start_day')
        end_day = body_data.get('end_day')
        order_id_list = body_data.get('order_id_list')
        if company_id and start_day and end_day and order_id_list:
            start_date = datetime.datetime.strptime(start_day, '%m/%d/%Y')
            end_date = datetime.datetime.strptime(end_day, '%m/%d/%Y')
            end_date = end_date.replace(hour=23, minute=59, second=59)

            company_price = Price.objects.filter(company_id=company_id).first()
            if not company_price:
                return JsonResponse({'error': 'В таблиці немає ціни для цього замовника'})
            company_nuances = CompanyWithNuances.objects.filter(company_id=company_id).first()

            check = Check()
            check.client_company_id = company_id
            check.order_list = order_id_list
            check.exchange = get_exchange_rate()
            if not check.exchange:
                return JsonResponse({'error': 'Не вдалося отримати курс'})
            if company_nuances:
                pass
            else:
                pass

