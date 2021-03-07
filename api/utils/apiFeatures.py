from rest_framework import serializers
class APIFeatures:
    def __init__(self,model,request):
        self.data = model.objects.all()
        self.request = request
        self.querySet=request.query_params
        self.serializer = APISerializer
        self.serializer.Meta.model=model    
        self.model = model

    def filter(self):
        fields=[]
        for field in self.model._meta.fields: 
            fields.append(field.name)
        query={}
        for field in fields:
            if field in self.querySet:
                query[field] = self.querySet[field]
        self.data=self.data.filter(**query)
        return self

    def sort(self):
        if 'sort' in self.querySet:      
            fields= tuple(self.querySet['sort'].split(','))
            self.data=self.data.order_by(*fields)
        return self

    def paginate(self):
        if 'page' in self.querySet and 'limit' in self.querySet:
            page =int( self.querySet['page']) or 1
            limit = int( self.querySet['limit']) or 10
            skip=page*limit - limit
            self.data=self.data[skip:skip+limit]
        return self

    def limitFields(self):
        if 'limitFields' in self.querySet:
            fields=self.querySet['limitFields'].split(',')
            self.serializer.Meta.fields=fields
        else:
            self.serializer.Meta.fields='__all__'
        return self

    def extract(self):
        output=self.serializer(data=self.data,many=True,context={'request': self.request})
        output.is_valid()
        return output.data

class APISerializer(serializers.ModelSerializer):
    
    class Meta:
        model=None
        fields='__all__'


