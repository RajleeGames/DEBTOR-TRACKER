from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Debtor(models.Model):
    name      = models.CharField(max_length=200, unique=True)
    phone     = models.CharField(max_length=20, blank=True)
    created   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def balance(self):
        # total goods taken MINUS total payments
        total_debits  = self.transactions.filter(kind='debit').aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_credits = self.transactions.filter(kind='credit').aggregate(models.Sum('amount'))['amount__sum'] or 0
        return total_debits - total_credits


class Transaction(models.Model):
    KIND_CHOICES = [
        ('debit',  'Goods Taken'),
        ('credit', 'Payment Made'),
    ]
    debtor    = models.ForeignKey(Debtor, related_name='transactions', on_delete=models.CASCADE)
    kind      = models.CharField(max_length=6, choices=KIND_CHOICES)
    amount    = models.DecimalField(max_digits=10, decimal_places=2)
    note      = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']




class Profile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    phone  = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
