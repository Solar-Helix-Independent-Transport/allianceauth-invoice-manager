from django_celery_beat.models import CrontabSchedule, PeriodicTask

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from allianceauth.eveonline.models import EveCorporationInfo

from . import __version__
from .app_settings import PAYMENT_CORP
from .models import Invoice


@login_required
def show_invoices(request):
    try:
        recipt_corp = EveCorporationInfo.objects.get(
            corporation_id=PAYMENT_CORP)
    except Exception:
        recipt_corp = "None"
    chars = request.user.character_ownerships.all().values_list('character')
    admin_invoices = Invoice.objects.visible_to(
        request.user).filter(paid=False).exclude(character__in=chars)
    invoices = Invoice.objects.visible_to(
        request.user).filter(paid=False, character__in=chars)
    outstanding_isk = invoices.aggregate(total_isk=Sum('amount'))
    admin_isk = admin_invoices.aggregate(total_isk=Sum('amount'))
    completed_invoices = Invoice.objects.visible_to(request.user).filter(
        paid=True, character__in=chars).order_by('-due_date')[:10]
    if outstanding_isk['total_isk'] is None:
        outstanding = 0
    else:
        outstanding = outstanding_isk['total_isk']

    ctx = {'invoices': invoices,
           'admin_invoices': admin_invoices,
           'admin_isk': admin_isk['total_isk'],
           'outstanding_isk': outstanding,
           'complete_invoices': completed_invoices,
           'recipt_corp': recipt_corp}

    return render(request, 'invoices/list.html', context=ctx)


@login_required
@permission_required('invoices.admin')
def show_admin(request):

    check_payments = PeriodicTask.objects.filter(
        task='invoices.tasks.check_for_payments', enabled=True).count()
    outstanding_payments = PeriodicTask.objects.filter(
        task='invoices.tasks.check_for_outstanding', enabled=True).count()

    context = {
        "check_payments": check_payments,
        "outstanding_payments": outstanding_payments,
    }
    return render(request, 'invoices/admin.html', context=context)


@login_required
@permission_required('invoices.admin')
def admin_create_tasks(request):
    schedule_check_payments, _ = CrontabSchedule.objects.get_or_create(minute='15,30,45',
                                                                       hour='*',
                                                                       day_of_week='*',
                                                                       day_of_month='*',
                                                                       month_of_year='*',
                                                                       timezone='UTC'
                                                                       )

    schedule_outstanding_payments, _ = CrontabSchedule.objects.get_or_create(minute='0',
                                                                             hour='12',
                                                                             day_of_week='*',
                                                                             day_of_month='*',
                                                                             month_of_year='*',
                                                                             timezone='UTC'
                                                                             )

    PeriodicTask.objects.update_or_create(
        task='invoices.tasks.check_for_payments',
        defaults={
            'crontab': schedule_check_payments,
            'name': 'Check For Invoice Outstanding Payments',
            'enabled': True
        }
    )
    # Lets check every 15Mins
    PeriodicTask.objects.update_or_create(
        task='invoices.tasks.check_for_outstanding',
        defaults={
            'crontab': schedule_outstanding_payments,
            'name': 'Check For ESI Payments made',
            'enabled': True
        }
    )

    messages.info(
        request, "Created/Reset Invoice Task to defaults")

    return redirect('invoices:admin')


@login_required
def react_main(request):
    # get available models
    return render(request, 'invoices/react_base_bs5.html', context={"version": __version__, "app_name": "invoices", "page_title": "Invoices"})
