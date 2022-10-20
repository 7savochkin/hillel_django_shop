import codecs
import csv

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from products.models import Product, Category


class ImportForm(forms.Form):
    csv_file = forms.FileField(validators=[FileExtensionValidator(['csv'])])

    def clean_csv_file(self):
        uploaded_file = self.cleaned_data['csv_file']
        reader = csv.DictReader(codecs.iterdecode(uploaded_file, 'utf-8'))
        product_list = []
        for row in reader:
            try:
                product_list.append(
                    Product(
                        name=row['name'],
                        description=row['description'],
                        price=row['price'],
                        sku=row['sku'],
                        category=Category.objects.get_or_create(
                            name=row['name'])[0]
                    )
                )
            except KeyError as error:
                raise ValidationError(error)
        if not product_list:
            raise ValidationError("Wrong file")
        return product_list

    def save(self):
        Product.objects.bulk_create(self.cleaned_data['csv_file'])
