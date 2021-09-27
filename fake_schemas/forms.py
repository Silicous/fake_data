from django import forms
from extra_views import InlineFormSetFactory

from .models import FakeSchemas, FakeSchemasColumn


class FakeSchemaForm(forms.ModelForm):
    class Meta:
        model = FakeSchemas
        fields = "__all__"

        widgets = {
            "author": forms.HiddenInput(),
            "name": forms.TextInput(),
            "delimiters": forms.Select(),
            "quotes": forms.Select(),
        }


class FakeSchemaColumnsForm(forms.ModelForm):
    class Meta:
        model = FakeSchemasColumn
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(),
            "order": forms.NumberInput(),
            "data_type": forms.Select(),
            "data_range_from": forms.NumberInput(),
            "data_range_to": forms.NumberInput(),
        }


class FakeSchemaColumnInline(InlineFormSetFactory):
    model = FakeSchemasColumn
    form_class = FakeSchemaColumnsForm
    fields = "__all__"

    factory_kwargs = {
        "extra": 1,
        "max_num": None,
        "can_order": False,
        "can_delete": True,
    }


class ExportDatasetForm(forms.Form):
    rows = forms.IntegerField(label="Rows", required=True)
