class _Config(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

# singleton
config = _Config()