from webbot.models import Location
import logging

logger = logging.getLogger(__name__)

# Внутри цикла, перед вызовом get_or_create


def process_and_save_address_data(raw_data):
    exclusion_keywords = ['д.', 'дом', 'зд', 'зд.', 'кв', 'кв.', 'д.', 'д', 'АО', 'корп.', 'стр.', '1а', '116а', 'этаж', 'офис']
    for raw_address in raw_data:
        hydra_id, address = raw_address.split(maxsplit=1)
        parts = [part.strip() for part in address.split(',') if part.strip()]

        parent = None
        for level, part in enumerate(parts, start=1):
            if any(keyword in part for keyword in exclusion_keywords):
                continue

            # logger.debug(f"Processing part: {part}, Level: {level}, Parent: {parent}")
            # print('suka')
            location, created = Location.objects.get_or_create(
                name=part,
                level=level,
                parent=parent,
                defaults={'hydra_id': hydra_id}
            )
            parent = location