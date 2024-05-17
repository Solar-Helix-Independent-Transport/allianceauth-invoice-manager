import logging

from django.db import models

logger = logging.getLogger(__name__)


class InvoiceQuerySet(models.QuerySet):
    def visible_to(self, user):
        # superusers get all visible
        if user.is_superuser:
            logger.debug('Returning all invoices for superuser %s.' % user)
            return self

        if user.has_perm('invoices.view_all'):
            logger.debug('Returning all invoices for %s.' % user)
            return self

        try:
            char = user.profile.main_character
            assert char
            # build all accepted queries
            queries = [models.Q(character__character_ownership__user=user)]
            if user.has_perm('invoices.view_alliance'):
                if char.alliance_id is not None:
                    queries.append(
                        models.Q(character__alliance_id=char.alliance_id))
                else:
                    queries.append(
                        models.Q(character__corporation_id=char.corporation_id))
            if user.has_perm('invoices.view_corp'):
                if user.has_perm('invoices.view_alliance'):
                    pass
                else:
                    queries.append(
                        models.Q(character__corporation_id=char.corporation_id))
            logger.debug('%s queries for user %s characters.' %
                         (len(queries), user))
            # filter based on queries
            query = queries.pop()
            for q in queries:
                query |= q
            return self.filter(query)
        except AssertionError:
            logger.debug(
                'User %s has no main character. Nothing visible.' % user)
            return self.none()


class InvoiceManager(models.Manager):
    def get_queryset(self):
        return InvoiceQuerySet(self.model, using=self._db).select_related('payment', 'character', 'character__character_ownership__user__profile__main_character')

    def visible_to(self, user):
        return self.get_queryset().visible_to(user)
