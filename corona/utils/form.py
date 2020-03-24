from wtforms import Form


def my_strip_filter(value):
    if value is not None and hasattr(value, "strip"):
        return value.strip()
    return value


class Form(Form):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get("filters", [])
            filters.append(my_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)
