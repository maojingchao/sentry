from __future__ import absolute_import

from rest_framework.response import Response

from sentry.auth import manager
from sentry.auth.providers.saml2 import SAML2Provider
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationAdminPermission
from sentry.api.serializers import serialize


class OrganizationAuthProvidersEndpoint(OrganizationEndpoint):
    permission_classes = (OrganizationAdminPermission, )

    def get(self, request, organization):
        """
        List available auth providers that are available to use for an Organization
        ```````````````````````````````````````````````````````````````````````````

        :pparam string organization_slug: the organization short name
        :auth: required
        """
        provider_list = []
        for k, v in manager:
            provider_list.append({
                'key': k,
                'name': v.name,
                'requiredFeature': v.required_feature,
                'disables2FA': issubclass(v, SAML2Provider),
            })

        return Response(serialize(provider_list, request.user))
