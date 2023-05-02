from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Server(models.Model):
    ip_address = models.GenericIPAddressField()
    server_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128, null=True)
    is_monitored = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True)
    passwordless = models.BooleanField(default=False)
    health_monitored = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def set_password(self, raw_pass):
        self.password = make_password(raw_pass)
    
    def check_password(self, raw_pass):
        return check_password(raw_pass), self.password
