from custom.models import Orders, OrderDampers, OrderFartuks, OrderPlaneSlices, OrderDeliveries, ClicheTechnologies, \
    PrintingCompanies, Companies, CompanyClients, Engravers
from rest_framework import serializers
from store.models import Materials




class OrderDampersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDampers
        fields = '__all__'


class OrderFartuksSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFartuks
        fields = '__all__'


class OrderPlaneSlicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPlaneSlices
        fields = '__all__'


class OrderDeliveriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDeliveries
        fields = '__all__'


class ClicheTechnologiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClicheTechnologies
        fields = '__all__'


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Materials
        fields = '__all__'


class PrintingCompaniesSerializer(serializers.ModelSerializer):
    id = CompaniesSerializer(read_only=True)

    class Meta:
        model = PrintingCompanies
        fields = '__all__'


class EngraversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engravers
        fields = '__all__'


class CompanyClientsSerializer(serializers.ModelSerializer):
    id = CompaniesSerializer(read_only=True)

    class Meta:
        model = CompanyClients
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    order_delivery = OrderDeliveriesSerializer(read_only=True)
    cliche_technology = ClicheTechnologiesSerializer(read_only=True)
    material = serializers.SerializerMethodField()
    printing_companies = PrintingCompaniesSerializer(read_only=True, source='printing_company')
    company_client = CompanyClientsSerializer(read_only=True)
    engravers = EngraversSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'

    def get_material(self, obj):
        # Получаем объект материала и сериализуем его
        if obj.material_id:
            material = Materials.objects.filter(id=obj.material_id).first()
            if material:
                return MaterialSerializer(material).data
        return None


