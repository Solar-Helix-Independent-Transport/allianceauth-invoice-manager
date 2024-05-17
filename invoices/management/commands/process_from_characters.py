from corptools.models import CharacterWalletJournalEntry

from django.core.management.base import BaseCommand

from invoices.models import Invoice


class Command(BaseCommand):
    help = 'Run Payments with Character Records'

    def handle(self, *args, **options):
        self.stdout.write("Checking for payments")

        invoices = Invoice.objects.filter(paid=False)
        refs = invoices.values_list('invoice_ref')
        payments = CharacterWalletJournalEntry.objects.filter(reason__in=refs,
                                                              amount__lt=0)
        payment_dict = {}
        for payment in payments:
            if payment.reason not in payment_dict:
                payment_dict[payment.reason] = []
            payment_dict[payment.reason].append(payment)

        self.stdout.write(f"Found {len(payment_dict)} Viable Payments")
        for invoice in invoices:
            self.stdout.write(f"Checking {invoice.invoice_ref}")
            if invoice.invoice_ref in payment_dict:
                self.stdout.write(
                    f"Payment Found! {invoice.invoice_ref}")
                payment_totals = 0
                for p in payment_dict[invoice.invoice_ref]:
                    payment_totals += p.amount * -1

                if payment_totals >= invoice.amount:
                    self.stdout.write(f"Payed! {invoice.invoice_ref}")
                    invoice.paid = True
                    # invoice.payment = payment_dict[invoice.invoice_ref][0]
                    invoice.save()
                    invoice.notify("Payment Received", "Paid")
