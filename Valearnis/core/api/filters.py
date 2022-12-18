from rest_framework.filters import OrderingFilter as BaseOrderingFilter


class OrderingFilter(BaseOrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view) or []

        if ordering:
            _ordering_with_id = ordering
            if 'id' not in ordering and '-id' not in ordering:
                _ordering_with_id = ordering + ['-id']

            return queryset.order_by(*_ordering_with_id)

        return queryset
