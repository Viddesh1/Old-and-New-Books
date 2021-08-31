from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


STATE_CHOICES = (
("Andhra Pradesh","Andhra Pradesh"),
("Assam","Assam"),
("Bihar","Bihar"),
("Karnataka","Karnataka"),
("Arunachal Pradesh","Arunachal Pradesh"),
("Kerala","Kerala"),
("Chhattisgarh","Chhattisgarh"),
("Uttar Pradesh","Uttar Pradesh"),
("Goa","Goa"),
("Gujarat","Gujarat"),
("Haryana","Haryana"),
("Himachal Pradesh","Himachal Pradesh"),
("Jammu and Kashmir","Jammu and Kashmir"),
("Jharkhand","Jharkhand"),
("West Bengal","West Bengal"),
("Madhya Pradesh","Madhya Pradesh"),
("Maharashtra","Maharashtra"),
("Manipur","Manipur"),
("Meghalaya","Meghalaya"),
("Mizoram","Mizoram"),
("Nagaland","Nagaland"),
("Orissa","Orissa"),
("Punjab","Punjab"),
("Rajasthan","Rajasthan"),
("Sikkim","Sikkim"),
("Tamil Nadu","Tamil Nadu"),
("Telangana","Telangana"),
("Tripura","Tripura"),
("Uttarakhand","Uttarakhand")
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
('O', 'Old_books'),
('N','New_books')
)

SUB_CATEGORY_CHOICES = (
    ('AA', 'Action_and_Adventure'),
    ('C', 'Classics'),
    ('CG', 'Comic_Book_or_Graphic_Novel'),
    ('DM', 'Detective_and_Mystery'),
    ('F', 'Fantasy'),
    ('HF', 'Historical_Fiction'),
    ('H', 'Horror'),
    ('LF', 'Literary_Fiction')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    sub_category = models.CharField(choices=SUB_CATEGORY_CHOICES, max_length=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = {
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
}

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Feedback(models.Model):
    feedback = models.CharField(max_length=500)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)