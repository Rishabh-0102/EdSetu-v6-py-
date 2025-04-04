from google.generativeai import configure, list_models

configure(api_key="AIzaSyAhPb-x252CQduuzsOEjX6kz3YXEN2tHJI")

models = list_models()
print([model.name for model in models])