from classrooms import models as classroom_models
from uuid import uuid4
import random, string

characters = string.ascii_letters + string.digits


async def generate_uid():
    gen = None
    while not gen or await classroom_models.get_classroom_by_uid(gen):
        gen = str(uuid4().hex)
    return gen


async def generate_entry_code():
    gen = None
    while not gen or (await classroom_models.get_classroom_by_entry_code(gen)):
        gen = ''.join(
        random.choice(characters) for i in range(7)
    )
    return gen