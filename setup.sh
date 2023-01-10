python ecommerce/manage.py makemigrations
python ecommerce/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python ecommerce/manage.py shell
python ecommerce/manage.py runserver 0.0.0.0:8000
