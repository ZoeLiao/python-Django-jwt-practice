from django.db import models


class User(models.Model):
    phone = models.CharField(
            max_length=10,
            db_index=True
        )
    password = models.CharField(
            max_length=10,
            db_index=True
        )

    class Meta:
