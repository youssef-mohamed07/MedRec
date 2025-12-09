from django.core.management.base import BaseCommand
from api.models import Medicine


class Command(BaseCommand):
    help = 'Load sample medicines data into database'

    def handle(self, *args, **kwargs):
        medicines_data = [
            {
                'code': 'MED001',
                'name_ar': 'بانادول',
                'name_en': 'Panadol',
                'scientific_name': 'Paracetamol 500mg',
                'manufacturer': 'GlaxoSmithKline',
                'description_ar': 'مسكن للألم وخافض للحرارة',
                'description_en': 'Pain reliever and fever reducer',
                'dosage': 'قرص واحد كل 4-6 ساعات (حد أقصى 4 جرام يومياً)',
                'side_effects': 'نادراً: غثيان، طفح جلدي، اضطرابات في الكبد عند الإفراط',
                'warnings': 'لا تتجاوز الجرعة الموصى بها. تجنب الكحول.',
                'category': 'مسكنات',
                'price': 15.50,
            },
            {
                'code': 'MED002',
                'name_ar': 'كونجستال',
                'name_en': 'Congestal',
                'scientific_name': 'Paracetamol + Pseudoephedrine',
                'manufacturer': 'Medical Union Pharmaceuticals',
                'description_ar': 'علاج لأعراض البرد والإنفلونزا',
                'description_en': 'Treatment for cold and flu symptoms',
                'dosage': 'قرص واحد 3 مرات يومياً',
                'side_effects': 'دوخة، جفاف الفم، أرق',
                'warnings': 'لا يستخدم مع أدوية ضغط الدم. تجنب القيادة.',
                'category': 'أدوية البرد والإنفلونزا',
                'price': 22.00,
            },
            {
                'code': 'MED003',
                'name_ar': 'فيفادول',
                'name_en': 'Fevadol',
                'scientific_name': 'Paracetamol 1000mg',
                'manufacturer': 'Spimaco',
                'description_ar': 'مسكن قوي للألم وخافض للحرارة',
                'description_en': 'Strong pain reliever and antipyretic',
                'dosage': 'قرص واحد كل 6-8 ساعات',
                'side_effects': 'نادراً: حساسية جلدية',
                'warnings': 'لا يستخدم لأكثر من 10 أيام بدون استشارة طبيب',
                'category': 'مسكنات',
                'price': 18.00,
            },
            {
                'code': 'MED004',
                'name_ar': 'بروفين',
                'name_en': 'Brufen',
                'scientific_name': 'Ibuprofen 400mg',
                'manufacturer': 'Abbott',
                'description_ar': 'مسكن للألم ومضاد للالتهاب',
                'description_en': 'Pain reliever and anti-inflammatory',
                'dosage': 'قرص واحد 3 مرات يومياً بعد الأكل',
                'side_effects': 'ألم في المعدة، غثيان، حرقة المعدة',
                'warnings': 'تجنب على معدة فارغة. لا يستخدم مع أمراض القلب.',
                'category': 'مضادات الالتهاب',
                'price': 25.00,
            },
            {
                'code': 'MED005',
                'name_ar': 'فيتامين سي 1000',
                'name_en': 'Vitamin C 1000',
                'scientific_name': 'Ascorbic Acid 1000mg',
                'manufacturer': 'Various',
                'description_ar': 'مكمل غذائي لتقوية المناعة',
                'description_en': 'Dietary supplement for immune system',
                'dosage': 'قرص واحد يومياً',
                'side_effects': 'نادراً: اضطرابات معوية خفيفة',
                'warnings': 'لا يتجاوز 2000 ملجم يومياً',
                'category': 'فيتامينات',
                'price': 35.00,
            },
            {
                'code': 'MED006',
                'name_ar': 'أنتينال',
                'name_en': 'Antinal',
                'scientific_name': 'Nifuroxazide 200mg',
                'manufacturer': 'Amoun',
                'description_ar': 'مطهر معوي لعلاج الإسهال',
                'description_en': 'Intestinal antiseptic for diarrhea',
                'dosage': 'قرص واحد 4 مرات يومياً',
                'side_effects': 'نادراً: حساسية',
                'warnings': 'يجب شرب سوائل كثيرة أثناء العلاج',
                'category': 'أدوية الجهاز الهضمي',
                'price': 20.00,
            },
            {
                'code': 'MED007',
                'name_ar': 'أوجمنتين',
                'name_en': 'Augmentin',
                'scientific_name': 'Amoxicillin + Clavulanic Acid',
                'manufacturer': 'GlaxoSmithKline',
                'description_ar': 'مضاد حيوي واسع المجال',
                'description_en': 'Broad-spectrum antibiotic',
                'dosage': 'قرص كل 12 ساعة لمدة 7 أيام',
                'side_effects': 'إسهال، غثيان، طفح جلدي',
                'warnings': 'يجب إكمال الكورس كاملاً. لا يستخدم بدون وصفة طبية.',
                'category': 'مضادات حيوية',
                'price': 65.00,
            },
            {
                'code': 'MED008',
                'name_ar': 'فلاجيل',
                'name_en': 'Flagyl',
                'scientific_name': 'Metronidazole 500mg',
                'manufacturer': 'Sanofi',
                'description_ar': 'مضاد للطفيليات والبكتيريا اللاهوائية',
                'description_en': 'Antiprotozoal and antibacterial',
                'dosage': 'قرص 3 مرات يومياً',
                'side_effects': 'طعم معدني في الفم، غثيان',
                'warnings': 'تجنب الكحول تماماً أثناء العلاج',
                'category': 'مضادات حيوية',
                'price': 28.00,
            },
        ]

        created_count = 0
        updated_count = 0

        for med_data in medicines_data:
            medicine, created = Medicine.objects.update_or_create(
                code=med_data['code'],
                defaults=med_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {medicine.code} - {medicine.name_ar}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated: {medicine.code} - {medicine.name_ar}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully processed {len(medicines_data)} medicines'))
        self.stdout.write(self.style.SUCCESS(f'  - Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  - Updated: {updated_count}'))
