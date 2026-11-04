_m=__import__('src.personas.context_awareness',fromlist=['*'])
globals().update({k:v for k,v in vars(_m).items() if not k.startswith('__')})

