import requests_mock
from django.test import TestCase, override_settings

from signals.apps.zds.exceptions import (
    CaseConnectionException,
    CaseNotCreatedException,
    DocumentConnectionException,
    DocumentNotCreatedException,
    StatusNotCreatedException
)
from signals.apps.zds.tasks import (
    add_document_to_case,
    add_status_to_case,
    connect_signal_to_case,
    create_case,
    create_document
)
from tests.apps.signals.factories import SignalFactory, SignalFactoryWithImage
from tests.apps.zds.factories import ZaakSignalFactory
from tests.apps.zds.mixins import ZDSMockMixin


class TestTasks(ZDSMockMixin, TestCase):
    @requests_mock.Mocker()
    def test_create_case_no_case(self, mock):
        self.get_mock(mock, 'zrc_openapi')
        self.post_mock(mock, 'zrc_zaak_create')

        signal = SignalFactory()
        signal = create_case(signal)
        self.assertTrue(hasattr(signal, 'zaak'))

    @requests_mock.Mocker()
    def test_create_case_with_case(self, mock):
        zaak_signal = ZaakSignalFactory()
        create_case(zaak_signal.signal)

    @requests_mock.Mocker()
    def test_create_case_with_error(self, mock):
        self.get_mock(mock, 'zrc_openapi')
        self.post_error_mock(mock, 'zrc_zaak_create')

        signal = SignalFactory()

        with self.assertRaises(CaseNotCreatedException):
            create_case(signal)

    @requests_mock.Mocker()
    def test_connect_signal_to_case(self, mock):
        self.get_mock(mock, 'zrc_openapi')
        self.post_mock(mock, 'zrc_zaak_create')
        self.post_mock(mock, 'zrc_zaakobject_create')

        signal = SignalFactory()
        create_case(signal)
        connect_signal_to_case(signal)

    @override_settings(ZRC_ZAAKOBJECT_TYPE='random')
    @requests_mock.Mocker()
    def test_connect_signal_to_case_error(self, mock):
        self.get_mock(mock, 'zrc_openapi')
        self.post_error_mock(mock, 'zrc_zaakobject_create')

        zaak_signal = ZaakSignalFactory()

        with self.assertRaises(CaseConnectionException):
            connect_signal_to_case(zaak_signal.signal)

    @requests_mock.Mocker()
    def test_add_status_to_case(self, mock):
        self.get_mock(mock, 'zrc_openapi')
        self.post_mock(mock, 'zrc_status_create')

        zaak_signal = ZaakSignalFactory()
        add_status_to_case(zaak_signal.signal)

    @requests_mock.Mocker()
    def test_add_status_to_case_with_error(self, mock):
        self.get_mock(mock, 'zrc_openapi')
        self.post_error_mock(mock, 'zrc_status_create')

        zaak_signal = ZaakSignalFactory()

        with self.assertRaises(StatusNotCreatedException):
            add_status_to_case(zaak_signal.signal)

    @requests_mock.Mocker()
    def test_create_document(self, mock):
        self.get_mock(mock, 'drc_openapi')
        self.post_mock(mock, 'drc_enkelvoudiginformatieobject_create')

        signal = SignalFactoryWithImage()
        ZaakSignalFactory(signal=signal)
        create_document(signal)

    @requests_mock.Mocker()
    def test_create_document_with_error(self, mock):
        signal = SignalFactory()

        with self.assertRaises(ValueError):
            create_document(signal)

    @requests_mock.Mocker()
    def test_create_document_not_created_exception(self, mock):
        self.get_mock(mock, 'drc_openapi')
        self.post_error_mock(mock, 'drc_enkelvoudiginformatieobject_create')

        signal = SignalFactoryWithImage()
        ZaakSignalFactory(signal=signal)

        with self.assertRaises(DocumentNotCreatedException):
            create_document(signal)

    @requests_mock.Mocker()
    def test_add_document_to_case(self, mock):
        self.get_mock(mock, 'drc_openapi')
        self.post_mock(mock, 'drc_enkelvoudiginformatieobject_create')
        self.post_mock(mock, 'drc_objectinformatieobject_create')

        signal = SignalFactoryWithImage()
        ZaakSignalFactory(signal=signal)
        create_document(signal)
        add_document_to_case(signal)

    @requests_mock.Mocker()
    def test_add_document_to_case_with_error(self, mock):
        self.get_mock(mock, 'drc_openapi')
        self.post_mock(mock, 'drc_enkelvoudiginformatieobject_create')
        self.post_error_mock(mock, 'drc_objectinformatieobject_create')

        signal = SignalFactoryWithImage()
        ZaakSignalFactory(signal=signal)
        create_document(signal)

        with self.assertRaises(DocumentConnectionException):
            add_document_to_case(signal)
