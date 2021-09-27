from celery import shared_task

from .models import FakeSchemas, ExportedDataset
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
# status=0 - START
# status=1 - OK
# status=2 - ERROR


@shared_task(bind=True)
def generate_csv_task(self, obj=None, rows=None):
    schema = FakeSchemas.objects.get(pk=int(obj))
    task_id = schema.id

    dataset = ExportedDataset(schema=schema, task_id=task_id, status=0)
    dataset.save()
    try:
        result = schema.generate_fake_data(rows=int(rows), uid=task_id)
        if result:
            dataset.download_link = result
            dataset.status = 1
            dataset.save()
        return True

    except Exception:
        dataset.status = 2
        dataset.save()
        raise
