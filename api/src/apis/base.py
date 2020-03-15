from flask.views import MethodView


class Base(MethodView):
    def options(self, *args, **kwargs):
        return None

    @staticmethod
    def get_namespace(request):
        return "{} {}".format(request.method, request.full_path)
