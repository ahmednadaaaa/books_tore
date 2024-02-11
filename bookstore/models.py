from django.db import models
from django.contrib.auth.models import User
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=190, null=True)
    email = models.CharField(max_length=190, null=True)
    phone = models.CharField(max_length=190, null=True)
    age = models.CharField(max_length=190, null=True)
    avatar = models.ImageField(blank=True, null=True, default="preson.png")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=190, null=True)

    def __str__(self):
       return self.name


class Book(models.Model):
    CATEGORY = (
        ('Classics','Classics'),
        ('Comic Book','Comic Book'),
        ('Fantasy','Fantasy'),
        ('Horror','Horror'),
        ('فلسفه', 'فلسفه'),
        ('روايات معاصرة','روايات معاصرة'),
        ('Horror','Horror'),

    )
    name = models.CharField(max_length=190, null=True)
    author = models.CharField(max_length=190, null=True)
    price = models.FloatField( null=True)
    category = models.CharField(max_length=190, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(blank=True, null=True, default="preson.png")

    def __str__(self):
         return self.name





class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    details = models.ManyToManyField(Book, through='OrderDetail')   # through جيب ال منج من خلال order details
    is_finished = models.BooleanField()
    total = 0
    items_count = 0

    def __str__(self):
        return 'User: ' + self.user.username + 'Order id' + str(self.id)


class OrderDetail(models.Model):
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return 'Order: {}, Book: {}, Order id: {}'.format(self.order.user.username, self.product.name, self.order.id)

    class Meta:
        ordering=['id'] # هيرتب العرض من القديم للاحدث


class Payment(models.Model):
        order = models.ForeignKey(Order, on_delete=models.CASCADE)
        shipment_address = models.CharField(max_length=150)
        shipment_phone = models.CharField(max_length=50)
        card_number = CardNumberField()
        expire = CardExpiryField()
        security_code = SecurityCodeField()

