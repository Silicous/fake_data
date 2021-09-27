import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.db import models
from faker import Faker

UserModel = get_user_model()


class FakeSchemas(models.Model):
    DELIMITERS = [
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        ("\t", "Tab (\t)"),
        (" ", "Space ( )"),
        ("|", "Vertical bar (|)"),
    ]

    QUOTES = [
        ('"', 'Double-quote (")'),
        ("'", "Single-quote (')"),
    ]

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="fake_schemas")
    name = models.CharField(blank=True, null=True, max_length=30)
    delimiters = models.CharField(max_length=1, choices=DELIMITERS, default=",")
    quotes = models.CharField(max_length=1, choices=QUOTES, default='"')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return f"/schemas/?{self.pk}"

    def generate_fake_data(self, rows=5, uid=None):
        import csv

        print('INSIDE OF THE GEN FUNC of MODEL')

        csv.register_dialect(
            "custom",
            delimiter=self.delimiters,
            quotechar=self.quotes,
            quoting=csv.QUOTE_ALL,
        )

        datafaker = Faker()

        def fake_data(data_type: int, val_range=(0, 100)):
            faker_methods = {
                0: datafaker.name(),
                1: datafaker.job(),
                2: datafaker.safe_email(),
                3: datafaker.paragraph(nb_sentences=val_range[1], variable_nb_sentences=False),
                4: datafaker.random_int(*val_range),
                5: datafaker.address(),
                6: datafaker.date(),
            }
            return faker_methods[data_type]

        columns = self.schema_column.all().values()
        fieldnames = [el["name"] for el in columns]

        try:
            os.mkdir(settings.MEDIA_ROOT)
        except OSError:
            print("error creating output folder")

        with default_storage.open(settings.MEDIA_ROOT + f"/{uid}_schema.csv", "w") as f:

            writer = csv.DictWriter(f, fieldnames=fieldnames, dialect="custom")
            writer.writeheader()

            for i in range(rows):
                row = {}
                for col in columns:

                    value = fake_data(col["data_type"])
                    if col["data_range_from"] and col["data_range_to"] and col["data_type"] in (6, 7):
                        value = fake_data(col["data_type"], val_range=(col["data_range_from"], col["data_range_to"]))

                    row[col["name"]] = value
                writer.writerow(row)

        return f"{settings.MEDIA_URL}{uid}_schema.csv"


class FakeSchemasColumn(models.Model):
    DATA_TYPES_CHOICES = [
        (0, "Full name"),
        (1, "Job"),
        (2, "Email"),
        (3, "Text"),
        (4, "Integer"),
        (5, "Address"),
        (6, "Date"),
    ]

    schema = models.ForeignKey(FakeSchemas, on_delete=models.CASCADE, related_name="schema_column")
    name = models.CharField(verbose_name="column name", blank=True, null=True, max_length=30)
    data_type = models.IntegerField(choices=DATA_TYPES_CHOICES, verbose_name="type")
    order = models.IntegerField(blank=True, default=0)
    data_range_from = models.IntegerField(blank=True, null=True, verbose_name="from")
    data_range_to = models.IntegerField(blank=True, null=True, verbose_name="to")

    class Meta:
        ordering = ["order"]


class ExportedDataset(models.Model):
    EXPORT_STATUS_CHOICES = [
        (0, "processing"),
        (1, "ready"),
        (2, "error"),
    ]
    schema = models.ForeignKey(FakeSchemas, on_delete=models.SET_NULL, related_name="schemadatasets", null=True,
                               blank=True, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0, choices=EXPORT_STATUS_CHOICES)
    download_link = models.URLField(null=True, blank=True)
    task_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-created"]
