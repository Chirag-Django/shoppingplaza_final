import random
import string


def random_string_gen(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_gen(instance):
    order_id= random_string_gen()
    Class_Object = instance.__class__
    q = Class_Object.objects.filter(order_id=order_id).exists()
    if q:
        return unique_order_id_gen(instance)
    return order_id
