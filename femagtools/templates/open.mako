  exit_on_error=true
  exit_on_end=${model.get('exit_on_end')}
  verbosity=2

model = '${model.get(['name'])}'
load_model(model)

