from webbot.models import Location
import logging

logger = logging.getLogger(__name__)

def part_needs_exclusion(part, exclusion_keywords):
    for keyword in exclusion_keywords:
        if keyword in part.split():  # Разделяем часть адреса на слова и проверяем точное совпадение
            return True
    return False

def process_and_save_address_data(raw_data):
    exclusion_keywords = ['д.', 'дом', 'зд', 'зд.', 'кв', 'кв.', 'д.', 'д', 'АО', 'корп.', 'стр.', '1а', '116а', 'этаж', 'офис']
    country_name = "Кыргызстан"

    for raw_address in raw_data:
        hydra_id, address = raw_address.split(maxsplit=1)
        print(hydra_id + '||||' + address)
        parts = [part.strip() for part in address.split(',') if part.strip()]

        parent = None
        for level, part in enumerate(parts, start=1):
            if part == country_name:
                continue
            if part_needs_exclusion(part, exclusion_keywords):
                print(f"Исключаем из обработки: {part}")
                continue

            location, created = Location.objects.get_or_create(
                name=part,
                level=level - 1,
                parent=parent,
                defaults={'hydra_id': hydra_id}
            )
            parent = location