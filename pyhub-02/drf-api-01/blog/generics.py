from django.shortcuts import render


class View:
    model = None

    def __init__(self, **kwargs):
        # self.model = Post
        # setattr(self, "model", Post)
        for k, v in kwargs.items():
            setattr(self, k, v)  # 인스턴스 변수로서 설정

    def get_queryset(self):
        return self.model.objects.all()

    def get_template_name(self):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return f"{app_name}/{model_name}_list.html"

    def get_context_data(self):
        model_name = self.model._meta.model_name
        return {
            f"{model_name}_list": self.get_queryset(),
        }

    @classmethod
    def as_view(cls, **initkwargs):
        def view(request):
            instance = cls(**initkwargs)
            template_name = instance.get_template_name()
            context_data = instance.get_context_data()
            return render(request, template_name, context_data)
        return view
