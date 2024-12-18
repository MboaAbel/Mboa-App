from django.db.models.signals import post_save
from django.conf import settings
from django.shortcuts import reverse

from django.db import models

msee = settings.AUTH_USER_MODEL
user = msee


class Ticket(models.Model):
        
        
        name = models.CharField(max_length=150, unique=True)
        qrcode = models.ImageField(upload_to='ticket-qrcodes/')


CATEGORY_CHOICES = (
        ('S', 'Shirt'),
        ('SW', 'Sport wear'),
        ('OW', 'Outwear')
)

LABEL_CHOICES = (
        ('P', 'primary'),
        ('S', 'secondary'),
        ('D', 'danger')
)

ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
)


class UserProfile(models.Model):
        user = msee
        stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
        one_click_purchasing = models.BooleanField(default=False)
       
        def __str__(self):
                return self.user.email



class Product(models.Model):
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name



class Item(models.Model):
        title = models.CharField(max_length=100)
        price = models.FloatField()
        discount_price = models.FloatField(blank=True, null=True)
        category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
        label = models.CharField(choices=LABEL_CHOICES, max_length=1)
        slug = models.SlugField()
        description = models.TextField()
        image = models.ImageField(upload_to='products_img',default='img/Mboa Academy.jpg')
        image01 = models.ImageField(upload_to='products_img',default='img/Mboa Academy.jpg')
        image02 = models.ImageField(upload_to='products_img',default='img/Mboa Academy.jpg')
        image03 = models.ImageField(upload_to='products_img',default='img/Mboa Academy.jpg')
        
        def __str__(self):
                return self.title
        
        def get_absolute_url(self):
                return reverse("product", kwargs={
                        'slug': self.slug
                })
        
        def get_add_to_cart_url(self):
                return reverse("add-to-cart", kwargs={
                        'slug': self.slug
                })
        
        def get_remove_from_cart_url(self):
                return reverse("remove-from-cart", kwargs={
                        'slug': self.slug
                })


class OrderItem(models.Model):
        user = msee
        ordered = models.BooleanField(default=False)
        item = models.ForeignKey(Item, on_delete=models.CASCADE)
        quantity = models.IntegerField(default=1)
        
        def __str__(self):
                return f"{self.quantity} of {self.item.title}"
        
        def get_total_item_price(self):
                return self.quantity * self.item.price
        
        def get_total_discount_item_price(self):
                return self.quantity * self.item.discount_price
        
        def get_amount_saved(self):
                return self.get_total_item_price() - self.get_total_discount_item_price()
        
        def get_final_price(self):
                if self.item.discount_price:
                        return self.get_total_discount_item_price()
                return self.get_total_item_price()


class Order(models.Model):
        user = msee
        ref_code = models.CharField(max_length=20, blank=True, null=True)
        items = models.ManyToManyField(OrderItem)
        start_date = models.DateTimeField(auto_now_add=True)
        ordered_date = models.DateTimeField()
        ordered = models.BooleanField(default=False)
        shipping_address = models.ForeignKey(
                'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
        billing_address = models.ForeignKey(
                'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
        payment = models.ForeignKey(
                'Payment', on_delete=models.SET_NULL, blank=True, null=True)
        coupon = models.ForeignKey(
                'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
        being_delivered = models.BooleanField(default=False)
        received = models.BooleanField(default=False)
        refund_requested = models.BooleanField(default=False)
        refund_granted = models.BooleanField(default=False)

        class Orders(models.Model):
                STATUS = (
                        ('Pending', 'Pending'),
                        ('Order Confirmed', 'Order Confirmed'),
                        ('Out for Delivery', 'Out for Delivery'),
                        ('Delivered', 'Delivered'),
                )
                user = msee
                product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
                email = models.CharField(max_length=50, null=True)
                address = models.CharField(max_length=500, null=True)
                mobile = models.CharField(max_length=20, null=True)
                order_date = models.DateField(auto_now_add=True, null=True)
                status = models.CharField(max_length=50, null=True, choices=STATUS)

        '''
		1. Item added to cart
		2. Adding a billing address
		(Failed checkout)
		3. Payment
		(Preprocessing, processing, packaging etc.)
		4. Being delivered
		5. Received
		6. Refunds
		'''
        
        def __str__(self):
                return self.user.email
        
        def get_total(self):
                total = 0
                for order_item in self.items.all():
                        total += order_item.get_final_price()
                if self.coupon:
                        total -= self.coupon.amount
                return total


class Address(models.Model):
        user = msee
        street_address = models.CharField(max_length=100)
        apartment_address = models.CharField(max_length=100)
        country = 'Kenya'
        zip = models.CharField(max_length=100)
        address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
        default = models.BooleanField(default=False)
        
        def __str__(self):
                return self.user.email
        
        class Meta:
                verbose_name_plural = 'Addresses'


class Payment(models.Model):
        stripe_charge_id = models.CharField(max_length=50)
        user = msee
        amount = models.FloatField()
        timestamp = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
                return self.user.username


class Coupon(models.Model):
        code = models.CharField(max_length=15)
        amount = models.FloatField()
        
        def __str__(self):
                return self.code


class Refund(models.Model):
        order = models.ForeignKey(Order, on_delete=models.CASCADE)
        reason = models.TextField()
        accepted = models.BooleanField(default=False)
        email = models.EmailField()
        
        def __str__(self):
                return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
        user = msee
        if created:
                userprofile = UserProfile.objects.create(user=instance)
        post_save.connect(userprofile_receiver, sender=user)


class Member(models.Model):
        user = msee
        Name = models.CharField(max_length=100)
        balance = models.FloatField(blank=True, null=True)
        category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
        label = models.CharField(choices=LABEL_CHOICES, max_length=1)
        slug = models.SlugField()
        bio = models.TextField()
        street_address = models.CharField(max_length=100)
        apartment_address = models.CharField(max_length=100)
        c_image = models.ImageField(upload_to='products_img', default='img/Mboa Academy.jpg')
        p_image = models.ImageField(upload_to='products_img', default='img/Mboa Academy.jpg')
        
        
        def __str__(self):
                return self.slug
        
        def get_absolute_url(self):
                return reverse("product", kwargs={
                        'slug': self.slug
                })
        
        def follow_url(self):
                return reverse("add-to-cart", kwargs={
                        'slug': self.slug
                })