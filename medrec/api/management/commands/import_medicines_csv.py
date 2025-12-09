from django.core.management.base import BaseCommand
from api.models import Medicine
import csv
import os


class Command(BaseCommand):
    help = 'Import medicines from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'Error: File not found: {csv_file_path}'))
            return

        created_count = 0
        updated_count = 0
        error_count = 0

        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Expected columns:
            # code, name_ar, name_en, scientific_name, manufacturer,
            # description_ar, description_en, dosage, side_effects,
            # warnings, category, price
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    medicine_data = {
                        'code': row.get('code', '').strip(),
                        'name_ar': row.get('name_ar', '').strip(),
                        'name_en': row.get('name_en', '').strip(),
                        'scientific_name': row.get('scientific_name', '').strip(),
                        'manufacturer': row.get('manufacturer', '').strip(),
                        'description_ar': row.get('description_ar', '').strip(),
                        'description_en': row.get('description_en', '').strip(),
                        'dosage': row.get('dosage', '').strip(),
                        'side_effects': row.get('side_effects', '').strip(),
                        'warnings': row.get('warnings', '').strip(),
                        'category': row.get('category', '').strip(),
                    }

                    # Handle price (can be empty)
                    price_str = row.get('price', '').strip()
                    if price_str:
                        try:
                            medicine_data['price'] = float(price_str)
                        except ValueError:
                            self.stdout.write(
                                self.style.WARNING(f'Row {row_num}: Invalid price "{price_str}", skipping')
                            )
                            medicine_data['price'] = None
                    else:
                        medicine_data['price'] = None

                    # Validate required fields
                    if not medicine_data['code']:
                        self.stdout.write(
                            self.style.ERROR(f'Row {row_num}: Missing code, skipping')
                        )
                        error_count += 1
                        continue

                    if not medicine_data['name_ar']:
                        self.stdout.write(
                            self.style.ERROR(f'Row {row_num}: Missing name_ar, skipping')
                        )
                        error_count += 1
                        continue

                    # Create or update medicine
                    medicine, created = Medicine.objects.update_or_create(
                        code=medicine_data['code'],
                        defaults=medicine_data
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Row {row_num}: Created {medicine.code} - {medicine.name_ar}')
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'↻ Row {row_num}: Updated {medicine.code} - {medicine.name_ar}')
                        )

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Row {row_num}: Error - {str(e)}')
                    )

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Import completed!'))
        self.stdout.write(self.style.SUCCESS(f'  - Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  - Updated: {updated_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  - Errors: {error_count}'))
        self.stdout.write('='*50)
