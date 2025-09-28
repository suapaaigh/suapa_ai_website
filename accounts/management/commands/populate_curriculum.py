from django.core.management.base import BaseCommand
from accounts.utils import initialize_ghanaian_curriculum

class Command(BaseCommand):
    help = 'Populate the database with Ghanaian curriculum data'

    def handle(self, *args, **options):
        self.stdout.write('Populating curriculum data...')
        try:
            initialize_ghanaian_curriculum()
            self.stdout.write(
                self.style.SUCCESS('Successfully populated curriculum data!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error populating curriculum data: {str(e)}')
            )