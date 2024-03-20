from django_filters import rest_framework as filters

from .models import ProductModel


class GeneralProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    available = filters.ChoiceFilter(choices=((True, "Yes"), (False, "No")))
    category = filters.CharFilter(field_name="category", lookup_expr="iexact")
    # info_type = filters.CharFilter(
    #     field_name="info__type", lookup_expr="exact", method="filter_few_values"
    # )
    # info = filters.CharFilter(method="filter_json_field")

    # def filter_few_values(self, queryset, name, value):
    #     few_values = value.split(",")
    #     return queryset.filter(**({f"{name}__in": few_values}))

    # def filter_json_field(self, queryset, name, value):

    #     filters = [pair.split(":") for pair in value.split(";")]

    #     json_filters = {}
    #     for key, val in filters:

    #         if key in json_filters:
    #             json_filters[key].append(val)
    #         else:
    #             json_filters[key] = [val]

    #     qs = queryset

    #     for key, val in json_filters.items():
    #         for value in val:
    #             if value.lower() == "true" or value.lower() == "false":
    #                 qs = qs.filter(**{f"info__{key}": value.lower() == "true"})
    #             elif "[" in value:
    #                 qs = qs.filter(**{f"info__{key}__contains": value[1:-1].split(",")})
    #             else:
    #                 qs = qs.filter(**({f"info__{key}__in": val[0].split(",")}))

    #         комент# qs = qs.filter(**({f'info__{key}__in':val[0].split(',')}))

    #     return qs

    class Meta:
        model = ProductModel
        fields = [
            "price",
            "available",
            "category",
        ]


class AllWillBeOneFilter(GeneralProductFilter):
    pass
