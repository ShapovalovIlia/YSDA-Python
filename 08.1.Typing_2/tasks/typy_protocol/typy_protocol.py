

class Gettable:
    pass


def get(container, index):
    if container:
        return container[index]

    return None
