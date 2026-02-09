from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def notexist():
    return {"error": "los datos no fueron encontrados"}


class SuperApiView(APIView):
    model = None
    serializer_class = None
    filter_fields = []

    def get(self, request, pk=None):
        # GET por ID (path param)
        if pk is not None:
            try:
                obj = self.model.objects.get(pk=pk)
                serializer = self.serializer_class(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except self.model.DoesNotExist:
                return Response(notexist(), status=status.HTTP_404_NOT_FOUND)

        # GET con filtros (query params)
        filters = {}
        for field in self.filter_fields:
            value = request.query_params.get(field)
            if value is not None:
                filters[field] = value

        queryset = self.model.objects.filter(**filters)

        if not queryset.exists():
            return Response(notexist(), status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response(notexist(), status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response(notexist(), status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(obj, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response(notexist(), status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)