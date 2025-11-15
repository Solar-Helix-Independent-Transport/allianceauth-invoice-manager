import logging
from typing import List

from ninja import NinjaAPI
from ninja.security import django_auth

from django.conf import settings
from django.db.models import BooleanField, Value

from allianceauth.eveonline.models import EveCorporationInfo

from . import models, schema
from .app_settings import PAYMENT_CORP

logger = logging.getLogger(__name__)


api = NinjaAPI(title="Invoice Manager API", version="0.0.1",
               urls_namespace='invoices:api', auth=django_auth,
               openapi_url=settings.DEBUG and "/openapi.json" or "")


@api.get(
    "account/unpaid",
    response={200: List[schema.Invoice]},
    tags=["Account"]
)
def get_account_invoices(request):
    chars = request.user.character_ownerships.all().values_list('character')
    invoices = models.Invoice.objects.visible_to(
        request.user).filter(paid=False, character__in=chars).order_by("due_date")
    paid = models.Invoice.objects.visible_to(
        request.user).filter(paid=True, character__in=chars).order_by("-due_date")
    output = []
    for i in invoices:
        output.append(i)
    for i in paid[:5]:
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
        request.user).filter(paid=False, character__character_ownership__isnull=False).exclude(
        character__in=chars).annotate(action=Value(request.user.has_perm('invoices.change_invoice'),
                                                   output_field=BooleanField()))
    return 200, admin_invoices


@api.get(
    "config/corp",
    response={200: schema.Corporation},
    tags=["Config"]
)
def get_payment_corp(request):
    return EveCorporationInfo.objects.get(corporation_id=PAYMENT_CORP)


@api.post(
    "admin/paid/{id}",
    response={200: str, 404: str, 403: str},
    tags=["admin"]
)
def post_mark_paid(request, id: int):
    perms = request.user.has_perm('invoices.change_invoice')
    if perms:
        inv = models.Invoice.objects.visible_to(request.user).filter(id=id)
        if inv.exists():
            inv = inv.first()
            inv.marked_paid_by = request.user.profile.main_character
            inv.paid = True
            inv.save()
            inv.notify(
                f"Invoice marked as paid by {request.user.profile.main_character}.")
            return 200, "Invoice Paid"
        return 404, "Invoice Not Found"
    else:
        return 403, "Permision Denied for User"
