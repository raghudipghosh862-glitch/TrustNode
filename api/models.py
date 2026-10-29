from django.db import models

# Create your models here.

class Bounty(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'), 
        ('funded', 'Funded (In Escrow)'), 
        ('completed', 'Completed')
    )
    title = models.CharField(max_length=255)
    success_criteria = models.TextField(help_text="Strict instructions for the AI reviewer")
    escrow_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    payout_batch_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class Submission(models.Model):
    bounty = models.ForeignKey(Bounty, on_delete=models.CASCADE, related_name='submissions')
    developer_paypal_email = models.EmailField(help_text="Where the AI sends the payout")
    code_content = models.TextField()
    ai_status = models.CharField(max_length=20, default='pending')
    ai_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission for {self.bounty.title}"
