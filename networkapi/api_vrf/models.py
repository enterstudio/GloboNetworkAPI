# -*- coding: utf-8 -*-
import logging

from _mysql_exceptions import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from networkapi.api_vrf.exceptions import VrfError
from networkapi.api_vrf.exceptions import VrfNotFoundError
from networkapi.filter.models import FilterNotFoundError
from networkapi.models.BaseModel import BaseModel


class Vrf(BaseModel):

    id = models.AutoField(
        primary_key=True,
        db_column='id'
    )
    vrf = models.TextField(
        max_length=45,
        db_column='vrf'
    )
    internal_name = models.TextField(
        max_length=45,
        db_column='internal_name'
    )

    log = logging.getLogger('Vrf')

    @classmethod
    def get_by_pk(cls, id_vrf):
        """Get Vrf by id.

        @return: Vrf.

        @raise VrfNotFoundError: Vrf is not registered.
        @raise VrfError: Failed to search for the Vrf.
        @raise OperationalError: Lock wait timeout exceed
        """
        try:
            return Vrf.objects.filter(id=id_vrf).uniqueResult()
        except ObjectDoesNotExist, e:
            raise VrfNotFoundError(
                e, u'Dont there is a Vrf by pk = %s.' % id_vrf)
        except OperationalError, e:
            cls.log.error(u'Lock wait timeout exceeded.')
            raise OperationalError(
                e, u'Lock wait timeout exceeded; try restarting transaction')
        except Exception, e:
            cls.log.error(u'Failure to search the Vrf.')
            raise VrfError(e, u'Failure to search the Vrf.')

    def create(self, authenticated_user):
        """Include new Vrf.

        @return: Id new Vrf

        @raise FilterNotFoundError: Dont' exist filter for pk searched
        """

        try:
            return self.save()

        except FilterNotFoundError, e:
            raise e
        except Exception:
            self.log.error(u'Fail on inserting Vrf.')

    @classmethod
    def update(cls, authenticated_user, pk, **kwargs):
        """Change some Vrf.

        @return: Nothing

        @raise VrfNotFoundError: It doesn't exist Vrf for searched pk.

        @raise CannotDissociateFilterError: Filter in use, can't be dissociated.
        """
        vrf = Vrf().get_by_pk(pk)

        try:
            try:
                Vrf.objects.get(id=pk)
            except Vrf.DoesNotExist:
                pass

            vrf.__dict__.update(kwargs)
            vrf.save(authenticated_user)

        except Exception, e:
            cls.log.error(u'Fail to change Vrf.')

    @classmethod
    def remove(cls, pk):
        """Remove vrf.

        @return: Nothing

        @raise VrfNotFoundError: It doesn' exist Vrf to searched id

        """
        vrf = Vrf().get_by_pk(pk)

        # Remove the vrf
        try:
            vrf.delete()
        except Exception, e:
            cls.log.error(u'Fail to remove Vrf.')

    class Meta (BaseModel.Meta):
        managed = True
        db_table = u'vrf'


class VrfVlanEquipment(BaseModel):

    id = models.AutoField(
        primary_key=True,
        db_column='id'
    )
    vrf = models.ForeignKey(
        Vrf,
        db_column='id_vrf',
        null=False
    )
    vlan = models.ForeignKey(
        'vlan.Vlan',
        db_column='id_vlan',
        null=False
    )
    equipment = models.ForeignKey(
        'equipamento.Equipamento',
        db_column='id_equipment',
        null=False
    )

    log = logging.getLogger('VrfVlanEquipment')

    class Meta (BaseModel.Meta):
        db_table = u'vrf_vlan_eqpt'
        managed = True
        unique_together = ('vlan', 'equipment')


class VrfEquipment(BaseModel):

    id = models.AutoField(
        primary_key=True,
        db_column='id'
    )
    vrf = models.ForeignKey(
        'api_vrf.Vrf',
        db_column='id_vrf',
        null=False
    )
    equipment = models.ForeignKey(
        'equipamento.Equipamento',
        db_column='id_equipment',
        null=False
    )
    internal_name = models.TextField(
        max_length=45,
        db_column='internal_name'
    )

    log = logging.getLogger('VrfVlanEquipment')

    class Meta (BaseModel.Meta):
        db_table = u'vrf_eqpt'
        managed = True
        unique_together = ('vrf', 'equipment')
