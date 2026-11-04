_m=__import__('src.personas.behavior_profile',fromlist=['*'])
globals().update({k:v for k,v in vars(_m).items() if not k.startswith('__')})

