from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    TYPE_EMPLOYEE = "employee"
    TYPE_CUSTOMER = "customer"

    USER_TYPE_CHOICES = ((TYPE_EMPLOYEE, "Employee"), (TYPE_CUSTOMER, "Customer"))
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)


class Product(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    price = models.PositiveIntegerField()
    quantity_in_stock = models.PositiveIntegerField()


class Bill(TimeStampedModel):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_bills",
        limit_choices_to=models.Q(user_type=User.TYPE_CUSTOMER),
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employee_bills",
        limit_choices_to=models.Q(user_type=User.TYPE_EMPLOYEE),
    )
    total_amount = models.PositiveIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id:
            self.total_amount = sum(
                detail.get_cost() for detail in self.billdetail_set.all()
            )
        else:
            self.total_amount = 0
        super(Bill, self).save(*args, **kwargs)


class BillDetail(TimeStampedModel):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_cost = models.PositiveIntegerField(default=0)
