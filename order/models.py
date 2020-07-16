import uuid
import decimal

from django.db import models

from client.models import ClientProfile, ClientAddress
from product.models import Product
from order.choices import OrderChoices


class OrderManager(models.Manager):

    def add_product_to_order(self, client, product, new_quantity):
        """
        Add product to client's in progress order
        """

        in_progress_order = self.__get_in_progress_order_or_create(client)

        in_order_product = in_progress_order.products.filter(
            order=in_progress_order, product=product)

        if in_order_product.count():
            in_order_product.get().update(
                product_quantity=new_quantity,
                product_price=product.price
            )
        else:
            ProductOrder.objects.create(
                order=in_progress_order,
                product=product,
                product_quantity=new_quantity,
                product_price=product.price
            )

    def __get_in_progress_order_or_create(self, client):
        """
        Get the client's in progress order or create a new one
        """
        in_progress_order = self.filter(
            client=client, status=OrderChoices.IN_PROGRESS)

        if in_progress_order.count():
            return in_progress_order.get()

        return self.create(client=client)


class Order(models.Model):
    """
    Client's order model
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    client = models.ForeignKey(
        ClientProfile,
        verbose_name="Client",
        related_name='orders',
        on_delete=models.DO_NOTHING
    )
    delivery_address = models.ForeignKey(
        ClientAddress,
        verbose_name="Delivery address",
        related_name='orders',
        on_delete=models.DO_NOTHING,
        null=True
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="Products",
        related_name='orders',
        through="ProductOrder"
    )
    date_created = models.DateTimeField(
        "Date the order was created"
    )
    date_updated = models.DateTimeField(
        "Last date the order was updated"
    )
    current_status = models.CharField(
        "Current status",
        max_length=11,
        default=OrderChoices.CONFIRMED,
        choices=OrderChoices.choices
    )
    full_price = models.DecimalField(
        "Full price",
        max_digits=10,
        decimal_places=2,
        default=decimal.Decimal(0.0)
    )

    objects = OrderManager()


class ProductOrder(models.Model):
    """
    Intermedian model between products and orders

    """
    order = models.ForeignKey(
        Order,
        related_name="productorder_order",
        on_delete=models.DO_NOTHING
    )
    product = models.ForeignKey(
        Product,
        related_name="productorder_product",
        on_delete=models.DO_NOTHING,
    )
    product_price = models.DecimalField(
        "Price",
        max_digits=10,
        decimal_places=2
    )
    product_quantity = models.PositiveIntegerField(
        "Quantity",
    )
    date_created = models.DateTimeField(
        "Date the product was included"
    )
    date_updated = models.DateTimeField(
        "Last date the product was updated"
    )
