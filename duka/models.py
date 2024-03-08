from django.db import models
from datetime import datetime
from django.conf import settings
# Create your models here.
CATEGORY_CHOICES = (
        ('PR', 'Premium'),
        ('LX', 'Luxury'),
        ('OW', 'Comfort'),
        ('EC', 'Economy'),
        ('BS', 'Basic')
)

state_choice = (
	('Nai','Nairobi'),
	('Ngo','Ngong'),
	('Ron','Rongai'),
	('Kaw','Kawangware')
)


# Create your models here.
class Car(models.Model):
		
		year_choice = []
		for r in range(2000, (datetime.now().year + 1)):
			year_choice.append((r, r))
		
		features_choices = (
			('Cruise Control', 'Cruise Control'),
			('Audio Interface', 'Audio Interface'),
			('Airbags', 'Airbags'),
			('Air Conditioning', 'Air Conditioning'),
			('Seat Heating', 'Seat Heating'),
			('Alarm System', 'Alarm System'),
			('ParkAssist', 'ParkAssist'),
			('Power Steering', 'Power Steering'),
			('Reversing Camera', 'Reversing Camera'),
			('Direct Fuel Injection', 'Direct Fuel Injection'),
			('Auto Start/Stop', 'Auto Start/Stop'),
			('Wind Deflector', 'Wind Deflector'),
			('Bluetooth Handset', 'Bluetooth Handset'),
		)
		
		door_choices = (
			('2', '2'),
			('3', '3'),
			('4', '4'),
			('5', '5'),
			('6', '6'),
		)
		
		car_title = models.CharField(max_length=255)
		state = models.CharField(choices=state_choice, max_length=100)
		city = models.CharField(max_length=100)
		color = models.CharField(max_length=100)
		model = models.CharField(max_length=100)
		year = models.IntegerField(('year'), choices=year_choice)
		condition = models.CharField(max_length=100)
		price = models.IntegerField()
		description = models.TextField()
		car_photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
		car_photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
		car_photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
		car_photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
		car_photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
		features = models.CharField(choices=features_choices, max_length=25)
		body_style = models.CharField(max_length=100)
		engine = models.CharField(max_length=100)
		transmission = models.CharField(max_length=100)
		interior = models.CharField(max_length=100)
		miles = models.IntegerField()
		doors = models.CharField(choices=door_choices, max_length=10)
		passengers = models.IntegerField()
		vin_no = models.CharField(max_length=100)
		milage = models.IntegerField()
		fuel_type = models.CharField(max_length=50)
		no_of_owners = models.CharField(max_length=100)
		is_featured = models.BooleanField(default=False)
		created_date = models.DateTimeField(default=datetime.now, blank=True)
		
		
		def __str__(self):
			return self.car_title
		
		
class Product(models.Model):
			name = models.CharField(max_length=200)
			slug = models.CharField(max_length=200)
			description = models.TextField()
			image = models.ImageField(upload_to='products_img')
			price = models.DecimalField(max_digits=10,decimal_places=2)
			category = models.CharField(choices=CATEGORY_CHOICES, max_length=2,default='Ngong')
			
		
			
class Cart(models.Model):
			item = models.ManyToManyField(Product)
