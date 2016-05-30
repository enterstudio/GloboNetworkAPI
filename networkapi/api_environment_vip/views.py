# -*- coding:utf-8 -*-
import logging
import urllib

from networkapi.ambiente.models import EnvironmentVip
from networkapi.api_environment_vip import exceptions, facade, serializers
from networkapi.api_environment_vip.permissions import Read
from networkapi.api_rest import exceptions as api_exceptions
from networkapi.util import logs_method_apiview, permission_classes_apiview


from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

log = logging.getLogger(__name__)


class OptionVipEnvironmentVipOneView(APIView):

    @permission_classes_apiview((IsAuthenticated, Read))
    @logs_method_apiview
    def get(self, request, *args, **kwargs):
        """
        Method to return option vip list by environment id
        Param environment_vip_id: environment id
        Return option vip object list
        """
        try:
            environment_vip_id = kwargs["environment_vip_id"]

            options_vip = facade.get_option_vip_by_environment_vip_ids([environment_vip_id])

            if options_vip:
                options_vip = options_vip[0]

            serializer_options = serializers.OptionVipEnvironmentVipSerializer(
                options_vip,
                many=True
            )
            return Response(serializer_options.data, status.HTTP_200_OK)
        except Exception, exception:
            log.error(exception)
            raise api_exceptions.NetworkAPIException()


class EnvironmentVipStepOneView(APIView):

    @permission_classes_apiview((IsAuthenticated, Read))
    @logs_method_apiview
    def get(self, request, *args, **kwargs):
        """
        Method to return finality, client or environment vip list.
        Param request.GET["finality"]: finality of environment(optional)
        Param request.GET["client"]: client of environment(optional)
        Param request.GET["environmentp44"]: environmentp44(optional)
        Return finality list: when request has no finality and client.
        Return client list: when request has only finality.
        Return environment vip list: when request has finality and client.
        Return object environment vip: when request has finality and client and environmentp44.
        """

        try:
            data = request.GET

            finality = data.get('finality')
            client = data.get('client')
            environmentp44 = data.get('environmentp44')

            if client != '' and finality != '' and environmentp44 != '':
                obj = EnvironmentVip().get_by_values(finality, client, environmentp44)
                evip_values = serializers.EnvironmentVipSerializer(
                    obj,
                    many=False
                ).data
            elif client != '' and finality != '':
                obj = EnvironmentVip().list_all_ambientep44_by_finality_and_cliente(finality, client)
                evip_values = serializers.EnvironmentVipSerializer(
                    obj,
                    many=True
                ).data
            elif finality != '':
                evip_values = EnvironmentVip().list_all_clientes_by_finalitys(finality)
            else:
                evip_values = EnvironmentVip().list_all_finalitys()

            return Response(evip_values, status=status.HTTP_200_OK)
        except Exception, exception:
            log.error(exception)
            raise api_exceptions.NetworkAPIException()


class EnvironmentVipView(APIView):

    @permission_classes_apiview((IsAuthenticated, Read))
    @logs_method_apiview
    def get(self, request, *args, **kwargs):
        """
        Method to return environment vip list.
        Param environment_vip_ids: environment_vip_ids
        """
        try:
            if not kwargs.get('environment_vip_ids'):
                raise NotImplemented()
            else:
                environment_vip_ids = kwargs['environment_vip_ids'].split(';')

                environments_vip = facade.get_environmentvip_by_ids(environment_vip_ids)

                if environments_vip:
                    environmentvip_serializer = serializers.EnvironmentVipSerializer(
                        environments_vip,
                        many=True
                    )
                    data = {
                        'environments_vip': environmentvip_serializer.data
                    }
                else:
                    raise exceptions.EnvironmentVipDoesNotExistException()

            return Response(data, status.HTTP_200_OK)

        except Exception, exception:
            log.exception(exception)
            raise api_exceptions.NetworkAPIException(exception)


class OptionVipEnvironmentTypeVipView(APIView):

    @permission_classes_apiview((IsAuthenticated, Read))
    @logs_method_apiview
    def get(self, request, *args, **kwargs):
        """
        Method to return option vip list by environment id and option vip type
        Param environment_vip_id: environment id
        Param type_option: environment id
        Return option vip object list
        """
        try:
            environment_vip_ids = kwargs["environment_vip_id"].split(';')
            type_option = urllib.unquote(kwargs["type_option"]).decode('utf8')
            search_list = list()

            for environment_vip_id in environment_vip_ids:
                search_list.append({
                    'environment_vip_id': environment_vip_id,
                    'type_option': type_option
                })

            options_vips = facade.get_option_vip_by_environment_vip_type(search_list)

            data = dict()
            data['optionsvip'] = list()
            for options_vip in options_vips:
                serializer_options = serializers.OptionVipSerializer(
                    options_vip,
                    many=True
                )
                data['optionsvip'].append(serializer_options.data)

            return Response(data, status.HTTP_200_OK)

        except Exception, exception:
            log.error(exception)
            raise api_exceptions.NetworkAPIException()


class TypeOptionEnvironmentVipView(APIView):

    @permission_classes_apiview((IsAuthenticated, Read))
    @logs_method_apiview
    def get(self, request, *args, **kwargs):
        """
        Method to return option vip list by environment id and option vip type
        Param environment_vip_id: environment id
        Param type_option: environment id
        Return option vip object list
        """
        try:
            environment_vip_ids = kwargs["environment_vip_id"].split(';')
            type_option_vip = facade.get_type_option_vip_by_environment_vip_ids(environment_vip_ids)

            return Response(type_option_vip, status.HTTP_200_OK)

        except Exception, exception:
            log.error(exception)
            raise api_exceptions.NetworkAPIException()