from django.db.models import QuerySet
from django.test import TestCase

# Create your tests here.
from rest_framework.response import Response
from rest_framework.settings import api_settings


class ListModelMixin(object):
    """
    List a queryset.
    """
    # The filter backend classes to use for queryset filtering
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    # 'DEFAULT_PAGINATION_CLASS': None
    # The style to use for queryset pagination.
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    # 'DEFAULT_FILTER_BACKENDS': ()

    def __init__(self,request):
        self.queryset = None
        self.serializer_class = None
        self.lookup_field = 'pk'
        self.lookup_url_kwarg = None
        self.request = request



    def list(self, request, *args, **kwargs):
        # 根据 filter_backends 过滤配置 对queryset过滤
        queryset = self.filter_queryset(self.get_queryset())
        """
        # filter_queryset() queryset = backend().filter_queryset(self.request, queryset, self)
        # filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
        # for backend in list(filter_backends)
        # 'DEFAULT_PAGINATION_CLASS': None
        # get_queryset() queryset = self.queryset
        """
        # 根据 pagination_class 分页配置 对查询集分页
        page = self.paginate_queryset(queryset)
        """
        # paginator = None if pagination_class is None else pagination_class
        # None if paginator is None else paginator.paginate_queryset(self.queryset, self.request, view=self)
        # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        # 'DEFAULT_FILTER_BACKENDS': ()
        """
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # 根据是否有分页，返回序列化数据

    # class GenericAPIView(views.APIView):
    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    @property
    def paginator(self):
        """
            是否有配置文件pagination_class
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }




