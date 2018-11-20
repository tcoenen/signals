from unittest import mock

from django.test import TestCase

from signals.apps.signals.models import create_initial, update_status
from tests.apps.signals.factories import SignalFactory, StatusFactory


class TestSignalReceivers(TestCase):

    @mock.patch('signals.apps.zds.signal_receivers.tasks', autospec=True)
    def test_signal_creation_handler(self, mocked_tasks):
        signal = SignalFactory.create()

        create_initial.send(
            sender=self.__class__,
            signal_obj=signal,
        )

        mocked_tasks.create_case.assert_called_once_with(signal=signal)
        mocked_tasks.connect_signal_to_case.assert_called_once_with(signal=signal)
        mocked_tasks.add_status_to_case.assert_called_once_with(signal=signal)

    @mock.patch('signals.apps.zds.signal_receivers.tasks', autospec=True)
    def test_status_update_handler(self, mocked_tasks):
        signal = SignalFactory.create()
        prev_status = signal.status

        new_status = StatusFactory.create(_signal=signal)
        signal.status = new_status
        signal.save()

        update_status.send(
            sender=self.__class__,
            signal_obj=signal,
            status=new_status,
            prev_status=prev_status,
        )

        mocked_tasks.add_status_to_case.assert_called_once_with(signal=signal)
