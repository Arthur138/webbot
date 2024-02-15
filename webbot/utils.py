from webbot.models import Location


def process_and_save_address_data(raw_data):
    for raw_address in raw_data:
        # Разделяем строку по запятым и удаляем пробелы
        parts = [part.strip() for part in raw_address.split(',') if part.strip()]

        # Исключаем номер дома (последний компонент), если он вам не нужен
        parts = parts[:-1] if parts[-1].startswith('д.') else parts

        parent = None
        for level, part in enumerate(parts, start=1):
            # Проверяем, существует ли уже такая локация с данным родителем
            location, created = Location.objects.get_or_create(
                name=part,
                defaults={'level': level, 'parent': parent, 'country': 'Кыргызстан'}
            )
            # Для следующего компонента текущий становится родителем
            parent = location



