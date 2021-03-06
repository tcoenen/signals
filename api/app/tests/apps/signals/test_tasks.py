from unittest import mock

from django.test import TestCase

from signals.apps.signals import tasks


class TestTaskSaveCSVFilesDatawarehouse(TestCase):

    @mock.patch('signals.apps.signals.tasks.save_csv_files_datawarehouse')
    def test_task_save_csv_files_datawarehouse(
            self, mocked_save_csv_files_datawarehouse):
        tasks.task_save_csv_files_datawarehouse()

        mocked_save_csv_files_datawarehouse.assert_called_once()
