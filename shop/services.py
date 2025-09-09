
def get_objects_all(model):
    return model.objects.all()


def get_objects_filter(model, **kwargs):
    return model.objects.filter(**kwargs)


def get_objects(model, **kwargs):
    return model.objects.get(**kwargs)