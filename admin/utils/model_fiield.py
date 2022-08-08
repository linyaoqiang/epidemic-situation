from django.apps import apps


def resolve_model_fields(app_name, model_name):
    model_obj = apps.get_model(app_name, model_name)
    field_dic = {}
    for field in model_obj._meta.fields:
        field_dic[field.name] = field.verbose_name
    return field_dic
