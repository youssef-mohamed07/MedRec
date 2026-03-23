import csv
from django.core.management.base import BaseCommand
from api.models import Medicine

class Command(BaseCommand):
    help = 'Import medicines from a comprehensive CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the comprehensive medicines CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    medicine, created = Medicine.objects.update_or_create(
                        code=row.get('code', '').strip() or f'MED{count+100}',
                        defaults={
                            'name_ar': row.get('name_ar', '').strip(),
                            'name_en': row.get('name_en', '').strip(),
                            'scientific_name': row.get('active_ingredients', '').strip(),  # Map to scientific_name directly for fallback
                            'active_ingredients': row.get('active_ingredients', '').strip(),
                            'concentration': row.get('concentration', '').strip(),
                            'alternatives': row.get('alternatives', '').strip(),
                            'region_availability': row.get('region_availability', '').strip(),
                            'manufacturer': row.get('manufacturer', '').strip(),
                            'packaging': row.get('packaging', '').strip(),
                            'price': row.get('price', 0) if row.get('price') else 0,
                            'side_effects': row.get('side_effects', '').strip(),
                            'warnings': row.get('warnings', '').strip(),
                            'description_ar': row.get('description_ar', '').strip(),
                            'category': row.get('category', '').strip(),
                        }
                    )
                    action = "Created" if created else "Updated"
                    self.stdout.write(self.style.SUCCESS(f'{action} {medicine.name_en}'))
                    count += 1
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported/updated {count} medicines'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
