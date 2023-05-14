from django.contrib import admin

# Register your models here.
from .models import Contact
from .models import Stock
from .models import Balance
from .models import Transaction
from .models import Portfolio
from .models import Level

admin.site.register(Contact)
admin.site.register(Stock)
admin.site.register(Balance)
admin.site.register(Transaction)
admin.site.register(Level)

