MAJOR = 0
MINOR = 92
PATCH = 1
STAGE = None

STRING = '.'.join(map(lambda v: str(v), filter(lambda v: v is not None, [MAJOR, MINOR, PATCH, STAGE])))
