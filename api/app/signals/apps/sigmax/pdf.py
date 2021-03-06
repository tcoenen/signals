"""
This module contains the PDF generation code used for Sigmax.
"""
import base64
import logging

import weasyprint
from django.template.loader import render_to_string

from signals.apps.signals.models import Signal

# Because weasyprint can produce a lot of warnings (unsupported
# CSS etc.) we ignore them.
logging.getLogger('weasyprint').setLevel(100)


def _render_html(signal: Signal):
    """Render given `Signal` with HTML template used for PDF generation.

    :param signal: Signal object
    :returns: HTML str
    """
    context = {
        'signal': signal,
        'image_url': signal.get_fqdn_image_crop_url()
    }
    return render_to_string('sigmax/pdf_template.html', context=context)


def _generate_pdf(signal: Signal):
    """Generate PDF to send to VoegZaakdocumentToe_Lk01.

    :param signal: Signal object
    :returns: base64 encoded data
    """
    html = _render_html(signal)
    pdf = weasyprint.HTML(string=html).write_pdf()

    return base64.b64encode(pdf)
