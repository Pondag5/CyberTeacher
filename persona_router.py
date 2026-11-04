_m=__import__('src.personas.persona_router',fromlist=['*'])
globals().update({k:v for k,v in vars(_m).items() if not k.startswith('__')})

