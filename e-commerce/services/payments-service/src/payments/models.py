from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("authorized", "Authorized"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    METHOD_CHOICES = [
        ("card", "Card"),
        ("bank", "Bank Transfer"),
        ("mobile", "Mobile Money"),
    ]

    user_id = models.CharField(max_length=64, null=True, blank=True)
    order_id = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="mobile")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    reference = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["order_id"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return f"Payment {self.reference} - {self.status}"
    
class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="transactions")
    gateway = models.CharField(max_length=80)
    gateway_reference = models.CharField(max_length=120)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.gateway} - {self.gateway_reference}"