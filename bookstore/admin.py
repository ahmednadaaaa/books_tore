from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *


admin.site.register(Customer)

@admin.register(Book)
class BookImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(Order)
class OrderImoprtExport(ImportExportModelAdmin):
    pass

@admin.register(Payment)
class PaymentImoprtExport(ImportExportModelAdmin):
    pass

#admin.site.register(Book)
@admin.register(OrderDetail)
class OrderDetailImoprtExport(ImportExportModelAdmin):
    pass
#admin.site.register(OrderDetail)
