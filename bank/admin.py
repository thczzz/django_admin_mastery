from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Customer
from django.urls import path, reverse


class CsvUploadForm(forms.Form):
    csv_upload = forms.FileField()


class BankAdminArea(admin.AdminSite):
    site_header = 'Bank Admin Area'
    login_template = 'admin/login.html'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload-csv/', self.upload_csv, name='upload-csv')
        ]
        return new_urls + urls

    def upload_csv(self, request):
        form = CsvUploadForm()

        if request.method == 'POST':
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded.')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(", ")
                name, balance = fields
                created = Customer.objects.update_or_create(name=name, balance=balance)

            return HttpResponseRedirect(reverse('BankAdmin:index'))

        return render(request, "admin/csv_upload.html", {'form': form})


bank_site = BankAdminArea(name='BankAdmin')
bank_site.register(Customer, CustomerAdmin, name='customer')