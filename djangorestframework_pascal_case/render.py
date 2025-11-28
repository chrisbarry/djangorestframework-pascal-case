from rest_framework.renderers import BrowsableAPIRenderer

from djangorestframework_pascal_case.settings import api_settings
from djangorestframework_pascal_case.util import pascalize


class PascalCaseJSONRenderer(api_settings.RENDERER_CLASS):
    json_underscoreize = api_settings.JSON_UNDERSCOREIZE

    def render(self, data, *args, **kwargs):
        return super().render(
            pascalize(data, **self.json_underscoreize), *args, **kwargs
        )


class PascalCaseBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, *args, **kwargs):
        return super(PascalCaseBrowsableAPIRenderer, self).render(
            pascalize(data, **api_settings.JSON_UNDERSCOREIZE), *args, **kwargs
        )


# Aliases for backwards compatibility
CamelCaseJSONRenderer = PascalCaseJSONRenderer
CamelCaseBrowsableAPIRenderer = PascalCaseBrowsableAPIRenderer
