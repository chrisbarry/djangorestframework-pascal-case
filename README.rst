=====================================
Django REST Framework JSON PascalCase
=====================================

PascalCase JSON support for Django REST framework.

This library is a fork of `djangorestframework-camel-case <https://github.com/vbabiy/djangorestframework-camel-case>`_
by Vitaly Babiy, modified to output PascalCase instead of camelCase. This is useful for
APIs that need to be compatible with .NET clients or frontends that expect PascalCase JSON keys.

============
Installation
============

Install from the local package::

    $ pip install -e ./djangorestframework-pascal-case

Add the render and parser to your django settings file.

.. code-block:: python

    # ...
    REST_FRAMEWORK = {

        'DEFAULT_RENDERER_CLASSES': (
            'djangorestframework_pascal_case.render.PascalCaseJSONRenderer',
            'djangorestframework_pascal_case.render.PascalCaseBrowsableAPIRenderer',
            # Any other renders
        ),

        'DEFAULT_PARSER_CLASSES': (
            # If you use MultiPartFormParser or FormParser, we also have a pascal case version
            'djangorestframework_pascal_case.parser.PascalCaseFormParser',
            'djangorestframework_pascal_case.parser.PascalCaseMultiPartParser',
            'djangorestframework_pascal_case.parser.PascalCaseJSONParser',
            # Any other parsers
        ),
    }
    # ...

Add query param middleware to django settings file.

.. code-block:: python

    # ...
    MIDDLEWARE = [
        # Any other middleware
        'djangorestframework_pascal_case.middleware.PascalCaseMiddleWare',
    ]
    # ...

=================
Swapping Renderer
=================

By default the package uses `rest_framework.renderers.JSONRenderer`. If you want
to use another renderer, the two possible are:

`drf_orjson_renderer.renderers.ORJSONRenderer` or
`drf_ujson.renderers.UJSONRenderer` or
`rest_framework.renderers.UnicodeJSONRenderer` for DRF < 3.0, specify it in your django
settings file.

.. code-block:: python

    # ...
    JSON_PASCAL_CASE = {
        'RENDERER_CLASS': 'drf_orjson_renderer.renderers.ORJSONRenderer'
    }
    # ...

=====================
Underscoreize Options
=====================


**No Underscore Before Number**


As raised in `this comment <https://github.com/krasa/StringManipulation/issues/8#issuecomment-121203018>`_
there are two conventions of snake case.

.. code-block:: text

    # Case 1 (Package default)
    V2Counter -> v_2_counter
    FooBar2 -> foo_bar_2

    # Case 2
    V2Counter -> v2_counter
    FooBar2 -> foo_bar2


By default, the package uses the first case. To use the second case, specify it in your django settings file.

.. code-block:: python

    JSON_PASCAL_CASE = {
        # ...
        'JSON_UNDERSCOREIZE': {
            'no_underscore_before_number': True,
        },
        # ...
    }

Alternatively, you can change this behavior on a class level by setting `json_underscoreize`:

.. code-block:: python

    from djangorestframework_pascal_case.parser import PascalCaseJSONParser
    from rest_framework.generics import CreateAPIView

    class NoUnderscoreBeforeNumberPascalCaseJSONParser(PascalCaseJSONParser):
        json_underscoreize = {'no_underscore_before_number': True}

    class MyView(CreateAPIView):
        queryset = MyModel.objects.all()
        serializer_class = MySerializer
        parser_classes = (NoUnderscoreBeforeNumberPascalCaseJSONParser,)

=============
Ignore Fields
=============

You can also specify fields which should not have their data changed.
The specified field(s) would still have their name change, but there would be no recursion.
For example:

.. code-block:: python

    data = {"my_key": {"do_not_change": 1}}

Would become:

.. code-block:: python

    {"MyKey": {"DoNotChange": 1}}

However, if you set in your settings:

.. code-block:: python

    JSON_PASCAL_CASE = {
        # ...
        "JSON_UNDERSCOREIZE": {
            # ...
            "ignore_fields": ("my_key",),
            # ...
        },
        # ...
    }

The `my_key` field would not have its data changed:

.. code-block:: python

    {"MyKey": {"do_not_change": 1}}

===========
Ignore Keys
===========

You can also specify keys which should *not* be renamed.
The specified field(s) would still change (even recursively).
For example:

.. code-block:: python

    data = {"unchanging_key": {"change_me": 1}}

Would become:

.. code-block:: python

    {"UnchangingKey": {"ChangeMe": 1}}

However, if you set in your settings:

.. code-block:: python

    JSON_PASCAL_CASE = {
        # ...
        "JSON_UNDERSCOREIZE": {
            # ...
            "ignore_keys": ("unchanging_key",),
            # ...
        },
        # ...
    }

The `unchanging_key` field would not be renamed:

.. code-block:: python

    {"unchanging_key": {"ChangeMe": 1}}

ignore_keys and ignore_fields can be applied to the same key if required.

=============
Running Tests
=============

To run the current test suite, execute the following from the root of the project::

    $ python -m unittest discover


=======
Credits
=======

This library is a fork of `djangorestframework-camel-case <https://github.com/vbabiy/djangorestframework-camel-case>`_
by Vitaly Babiy (vbabiy86@gmail.com).

=======
License
=======

* Free software: BSD license
