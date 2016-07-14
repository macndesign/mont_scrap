from channels import Channel
from django.shortcuts import render
from rest_framework import (
    viewsets,
    filters,
)
from .serializers import AuctionSerializer, CompanySerializer, LotSerializer, ImagesSerializer
from .pagination import ResultSetPagination
from .validations import company_query_schema
from filters.mixins import (
    FiltersMixin,
)
from .models import Company, Auction, Lot, Images


def extract(request):
    msg = {}
    Channel('extract').send(msg)
    return render(request, 'scrap/extract.html', {})


class CompanyViewSet(FiltersMixin, viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = CompanySerializer
    pagination_class = ResultSetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name')
    ordering = ('id',)

    # add a mapping of query_params to db_columns(queries)
    filter_mappings = {
        'id': 'id',
        'name': 'name__icontains',
        'description': 'description__icontains',
        'auction_id': 'teams',
    }

    # add validation on filters
    filter_validation_schema = company_query_schema

    def get_queryset(self):
        """
        Optionally restricts the queryset by filtering against
        query parameters in the URL.
        """
        query_params = self.request.query_params
        queryset = Company.objects.prefetch_related(
            'auction_set'  # use prefetch_related to minimize db hits.
        ).all()

        # This dict will hold filter kwargs to pass in to Django ORM calls.
        db_filters = {}

        # update filters dict with incoming query params and then pass as
        # **kwargs to queryset.filter()
        db_filters.update(
            self.get_queryset_filters(
                query_params
            )
        )
        return queryset.filter(**db_filters)
