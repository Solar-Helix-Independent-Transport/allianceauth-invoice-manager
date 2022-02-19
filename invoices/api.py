from typing import List
from allianceauth import notifications
from corptools import app_settings
from django.utils.timezone import activate

from ninja import NinjaAPI, Form, main
from ninja.security import django_auth
from ninja.responses import codes_4xx

from allianceauth.eveonline.models import EveCorporationInfo
from django.core.exceptions import PermissionDenied
from django.db.models import F, Sum, Q
from allianceauth.eveonline.models import EveCharacter
from django.conf import settings
from .app_settings import PAYMENT_CORP

from . import models
from . import schema

import logging

logger = logging.getLogger(__name__)


api = NinjaAPI(title="Invoice Manager API", version="0.0.1",
               urls_namespace='invoices:api', auth=django_auth, csrf=True,
               openapi_url=settings.DEBUG and "/openapi.json" or "")


@api.get(
    "account/unpaid",
    response={200: List[schema.Invoice]},
    tags=["Account"]
)
def get_account_invoices(request):
    chars = request.user.character_ownerships.all().values_list('character')
    invoices = models.Invoice.objects.visible_to(
        request.user).filter(paid=False, character__in=chars)
    paid = models.Invoice.objects.visible_to(
        request.user).filter(paid=True, character__in=chars)[:5]
    output = []
    for i in invoices:
        output.append(i)
    for i in paid:
        output.append(i)

    return 200, output


@api.get(
    "account/visible",
    response={200: List[schema.Invoice]},
    tags=["Account"]
)
def get_visible_invoices(request):
    chars = request.user.character_ownerships.all().values_list('character')
    admin_invoices = models.Invoice.objects.visible_to(
        request.user).filter(paid=False).exclude(character__in=chars)
    return 200, admin_invoices


@api.get(
    "config/corp",
    response={200: schema.Corporation},
    tags=["Config"]
)
def get_payment_corp(request):
    return EveCorporationInfo.objects.get(corporation_id=PAYMENT_CORP)
