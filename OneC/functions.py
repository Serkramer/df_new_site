import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from custom.models import CompanyOurBrands, Orders, CompanyClients


def get_exchange_rate():
    headers = {
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
      'cookie': 'visid_incap_2741169=8WkrCdvDTMeu8ZFgdPccXIOe3mIAAAAAQUIPAAAAAAAOrxu296SH1LUf9KM9wK96; incap_ses_273_2741169=OdoZJxNs/AGPP89byuTJAzc+M2MAAAAA3LAdXoMyvUD3ZYsZJN4KJA==; nlbi_2741169=MmDtdEJilnh4dZXRIBZ9ygAAAABKM5GeG5vxjrbTBgLyKw18; _ga=GA1.3.1044478189.1664302666; _gid=GA1.3.485875529.1664302666'
    }

    nbu_rates = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange',
                             params='json', headers=headers).json()
    for i in range(len(nbu_rates)):
        if nbu_rates[i]['cc'] == 'EUR':
            nbu_eur_rate = nbu_rates[i]['rate']
            rate = round(nbu_eur_rate + (nbu_eur_rate * 0.02), 4)
            return rate
    return 0


def create_xml(company, our_company, order_list):
    # Создание корневого элемента
    root = ET.Element('ZVIT')

    # TRANSPORT
    transport = ET.SubElement(root, 'TRANSPORT')
    ET.SubElement(transport, 'VERSION').text = '4.1'
    ET.SubElement(transport, 'CREATEDATE').text = '16.10.2024'

    # ORG
    org = ET.SubElement(root, 'ORG')

    # ORG -> FIELDS
    org_fields = ET.SubElement(org, 'FIELDS')
    ET.SubElement(org_fields, 'EDRPOU').text = '39148764'

    # ORG -> CARD
    card = ET.SubElement(org, 'CARD', RTFDOC='1')

    # ORG -> CARD -> FIELDS
    card_fields = ET.SubElement(card, 'FIELDS')
    fields_data = {
        'DOCID': 'D8CD1246-7C93-47DB-BB89-27FD5646535D',
        'OUTID': '',
        'GLOBALTMPLID': 'e05dcb11-6d5c-4af3-bc32-059a126bdb77',
        'TMPLEDRPOUOWNER': '831111111',
        'DOCNAME': 'Рахунок (ціна без ПДВ)',
        'CHARCODE': '1С82РАХ0',
        'PARTCODE': '7',
        'GRPID': '',
        'NOTATION': '',
        'SIGNERNAME': '',
        'SDOCTYPE': '10103',
        'PCTTYPE': '-1',
        'AUTHORNAME': 'Admin',
        'PEDRPOU': '02944828',
        'COMMENT': '',
        'CRTDATE': '16.10.2024'
    }

    for field, value in fields_data.items():
        ET.SubElement(card_fields, field).text = value

    # ORG -> CARD -> DOCUMENT
    document = ET.SubElement(card, 'DOCUMENT')

    # ORG -> CARD -> DOCUMENT -> ROW
    rows_data = [
        {'LINE': '0', 'TAB': '0', 'NAME': 'DOCDATE', 'VALUE': '16.10.2024 00:00:00'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'DOCSUM', 'VALUE': '600'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'DOCSUM_TEXT', 'VALUE': '600'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'DOG_DATA_T', 'VALUE': 'від'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'DOG_DATE', 'VALUE': '01.01.2024 00:00:00'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'DOG_NUM', 'VALUE': '123456'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'DOG_NUM_T', 'VALUE': '№'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'FIELD1', 'VALUE': '20.10.2024 00:00:00'},
        {'LINE': '0', 'TAB': '0', 'NAME': 'FIRM_ADR',
         'VALUE': 'вулиця Березинська, буд. 80, м. ДНІПРО, ДНІПРОПЕТРОВСЬКА обл., 49130, Україна'},
        # Добавить остальные строки...
    ]

    for row in rows_data:
        row_element = ET.SubElement(document, 'ROW', LINE=row['LINE'], TAB=row['TAB'], NAME=row['NAME'])
        ET.SubElement(row_element, 'VALUE').text = row['VALUE']

    # Форматирование XML с отступами
    xml_str = ET.tostring(root, encoding='windows-1251').decode('windows-1251')
    xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ", encoding='windows-1251')

    # Запись в файл
    with open('output.xml', 'wb') as f:
        f.write(xml_pretty_str)


company = CompanyClients.objects.get(id__okpo=32566124)
our_company = CompanyOurBrands.objects.get(id__okpo=41322471)
order_list = Orders.objects.filter(company_client=company)

# Вызов функции
# create_xml(company, our_company, order_list)
