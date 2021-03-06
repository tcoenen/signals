import copy
from datetime import timedelta

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.utils import timezone
from xmlunittest import XmlTestMixin

from signals.apps.sigmax.outgoing import (
    SIGMAX_REQUIRED_ADDRESS_FIELDS,
    SIGMAX_STADSDEEL_MAPPING,
    _address_matches_sigmax_expectation,
    _generate_creeerZaak_Lk01,
    _generate_omschrijving,
    _generate_voegZaakdocumentToe_Lk01
)
from signals.apps.signals.models import Priority
from tests.apps.signals.factories import SignalFactory, SignalFactoryValidLocation
from tests.apps.signals.valid_locations import STADHUIS


class TestOutgoing(TestCase, XmlTestMixin):

    def test_generate_creeerZaak_Lk01(self):
        current_tz = timezone.get_current_timezone()
        location = Point(4.1234, 52.1234)
        signal = SignalFactory.create(incident_date_end=None, location__geometrie=location)

        xml_message = _generate_creeerZaak_Lk01(signal)

        self.assertXmlDocument(xml_message)
        self.assertIn(
            '<StUF:referentienummer>{}</StUF:referentienummer>'.format(signal.sia_id),
            xml_message)
        self.assertIn(
            '<StUF:tijdstipBericht>{}</StUF:tijdstipBericht>'.format(
                signal.created_at.astimezone(current_tz).strftime('%Y%m%d%H%M%S')),
            xml_message)
        self.assertIn(
            '<ZKN:startdatum>{}</ZKN:startdatum>'.format(
                signal.incident_date_start.astimezone(current_tz).strftime('%Y%m%d')),
            xml_message)
        incident_date_end = signal.created_at + timedelta(days=3)
        self.assertIn(
            '<ZKN:einddatumGepland>{}</ZKN:einddatumGepland>'.format(
                incident_date_end.astimezone(current_tz).strftime('%Y%m%d')),
            xml_message)
        self.assertIn(
            '<StUF:extraElement naam="Ycoordinaat">{}</StUF:extraElement>'.format(location.y),
            xml_message)
        self.assertIn(
            '<StUF:extraElement naam="Xcoordinaat">{}</StUF:extraElement>'.format(location.x),
            xml_message)

    def test_generate_creeerZaak_Lk01_priority_high(self):
        current_tz = timezone.get_current_timezone()
        signal = SignalFactory.create(incident_date_end=None,
                                      priority__priority=Priority.PRIORITY_HIGH)

        xml_message = _generate_creeerZaak_Lk01(signal)

        self.assertXmlDocument(xml_message)
        incident_date_end = signal.created_at + timedelta(days=1)
        self.assertIn(
            '<ZKN:einddatumGepland>{}</ZKN:einddatumGepland>'.format(
                incident_date_end.astimezone(current_tz).strftime('%Y%m%d')),
            xml_message)

    def test_generate_voegZaakdocumentToe_Lk01(self):
        signal = SignalFactoryValidLocation.create()
        xml_message = _generate_voegZaakdocumentToe_Lk01(signal)
        self.assertXmlDocument(xml_message)

        self.assertIn(
            f'<ZKN:identificatie>{signal.sia_id}</ZKN:identificatie>',
            xml_message
        )

    def test_generate_voegZaakdocumentToe_Lk01_escaping(self):
        poison = SignalFactoryValidLocation.create()
        poison.text = '<poison>tastes nice</poison>'
        xml_message = _generate_voegZaakdocumentToe_Lk01(poison)
        self.assertTrue('<poison>' not in xml_message)


class TestGenerateOmschrijving(TestCase):
    def setUp(self):
        self.signal = SignalFactoryValidLocation(priority__priority=Priority.PRIORITY_HIGH)

    def test_generate_omschrijving(self):
        stadsdeel = self.signal.location.stadsdeel
        correct = 'SIA-{} URGENT {} {}'.format(
            self.signal.pk,
            SIGMAX_STADSDEEL_MAPPING.get(stadsdeel, 'SD--'),
            self.signal.location.short_address_text
        )

        self.assertEqual(_generate_omschrijving(self.signal), correct)

    def test_generate_omschrijving_no_stadsdeel(self):
        # test that we get SD-- as part of the omschrijving when stadsdeel is missing
        self.signal.location.stadsdeel = None
        self.signal.location.save()

        correct = 'SIA-{} URGENT {} {}'.format(
            self.signal.pk,
            'SD--',
            self.signal.location.short_address_text
        )

        self.assertEqual(_generate_omschrijving(self.signal), correct)


class TestAddressMatchesSigmaxExpectation(TestCase):
    def setUp(self):
        self.valid_address_dict = copy.copy(STADHUIS)  # has more fields than Location.address, so:
        self.valid_address_dict.pop('lon')
        self.valid_address_dict.pop('lat')
        self.valid_address_dict.pop('buurt_code')
        self.valid_address_dict.pop('stadsdeel')

    def test_full_valid(self):
        address_dict = copy.copy(self.valid_address_dict)

        self.assertEqual(True, _address_matches_sigmax_expectation(address_dict))

    def test_minimum_valid(self):
        address_dict = copy.copy(self.valid_address_dict)
        address_dict = {
            k: v for k, v in address_dict.items() if k in SIGMAX_REQUIRED_ADDRESS_FIELDS
        }

        self.assertEqual(True, _address_matches_sigmax_expectation(address_dict))

    def test_empty(self):
        self.assertEqual(False, _address_matches_sigmax_expectation({}))

    def test_invalid(self):
        address_dict = copy.copy(self.valid_address_dict)
        address_dict.pop('woonplaats')
        self.assertEqual(False, _address_matches_sigmax_expectation(address_dict))

        address_dict = copy.copy(self.valid_address_dict)
        address_dict.pop('openbare_ruimte')
        self.assertEqual(False, _address_matches_sigmax_expectation(address_dict))

        address_dict = copy.copy(self.valid_address_dict)
        address_dict.pop('huisnummer')
        self.assertEqual(False, _address_matches_sigmax_expectation(address_dict))

    def test_invalid_because_of_whitespace_values(self):
        address_dict = copy.copy(self.valid_address_dict)
        address_dict['woonplaats'] = ' '
        self.assertEqual(False, _address_matches_sigmax_expectation(address_dict))

        address_dict = copy.copy(self.valid_address_dict)
        address_dict['woonplaats'] = ' '
        self.assertEqual(False, _address_matches_sigmax_expectation(address_dict))

        address_dict = copy.copy(self.valid_address_dict)
        address_dict['woonplaats'] = ' '
        self.assertEqual(False, _address_matches_sigmax_expectation(address_dict))

    def test_none_value(self):
        # simulate empty address field
        self.assertEqual(False, _address_matches_sigmax_expectation(None))
        self.assertEqual(False, _address_matches_sigmax_expectation({}))
