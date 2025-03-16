from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select


class PatchedFilter(Filter):
    def sort(self, query) -> select:
        for field_name, _ in self.filtering_fields:
            field_value = getattr(self, field_name)
            if isinstance(field_value, Filter):
                query = field_value.sort(query)
        return super().sort(query)

    @property
    def filtering_fields(self):
        fields = self.model_dump(exclude_none=True)
        fields.pop(self.Constants.ordering_field_name, None)
        return fields.items()
