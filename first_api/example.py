## example get post,

class JobPoint(APIView):
"""
signup user general
"""
permission_classes = (permissions.IsAuthenticated,)


def get_point(self, pk):
        try:
            return Point.objects.get(pk=pk)
        except:
            response_data = {'status': 'fail', 'title': QUERY_FAIL, 'message': QUERY_FAIL_MESSAGE}
            return response_data

def get(self, request, pk=None, format=None):

    if pk:
        point = get_point(pk)
        if type(point) == type({}):
            return Response(point)
        serializer = PointSerializer(instance=point)
        response_get = serializer.data
        response_get['status'] = "success"
        response_get['title'] = ""
        response_get['message'] = ""
        return Response(response_get)

    response_get = {'status': 'fail', 'title': QUERY_FAIL, 'message': QUERY_FAIL_MESSAGE}
    return Response(response_get)

def post(self, request, format=None):
    """
    {
        "list_point" : 1,
        "name": "home_1",
        "lat": "13.721525",
        "lon": "100.783052"
    }
    """

    try:
        authen = request.META['HTTP_AUTHORIZATION']
        token = authen.replace("token ", "")
        q_token = Token.objects.get(key=token)
        q_user = q_token.user
        q_guard = SecurityGuard.objects.get(username=q_user)
        if q_guard.type_guard_id != 1 and q_guard.type_guard_id != 2:
            response_data_post = {'status': STATUS_FAIL, 'title': ADD_FAIL, 'message': ADD_FAIL_MESSAGE}
            return Response(response_data_post)
    except Exception as exc:
        print(exc)
        response_data_post = {'status': STATUS_FAIL, 'title': ADD_FAIL, 'message': ADD_FAIL_MESSAGE}
        return Response(response_data_post)

    data = request.data
    serializer = PointSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        response_post = serializer.data
        response_post['status'] = "success"
        response_post['title'] = ""
        response_post['message'] = ""
        return Response(response_post, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def put(self, request, pk=None, format=None):

    _status = request.data.get('status', "YES")
    if pk:
        point = get_point(pk)
        if type(point) == type({}):
            return Response(point)
        point.status = _status
        try:
            point.save()
            response_put = {'status': 'success', 'title': "", 'message': ""}
        except Exception as e:
            print(e)
            response_put = {'status': 'fail', 'title': UPDATE_POINT_FAIL, 'message': UPDATE_POINT_FAIL_MESSAGE}

        return Response(response_put)

    response_put = {'status': 'fail', 'title': UPDATE_POINT_FAIL, 'message': UPDATE_POINT_FAIL_MESSAGE}
    return Response(response_put)

def delete(self, request, pk=None, format=None):
    point = get_point(pk)
    if type(point) == type({}):
        return Response(point)
    point.delete()
    response_delete = {'status': 'success', 'title': "", 'message': ""}
    return Response(response_delete, status=status.HTTP_204_NO_CONTENT)

##example serializer with create additinal data

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('pk', 'zone', 'name', 'lat', 'lon', 'status')

    def create(self, validated_data):
        _datetime = datetime.datetime.now()
        point = Point.objects.create(last_update=_datetime, **validated_data)
        return point

##example serializer with many to many value 
class QRcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeScan
        fields = ('pk', 'code', 'number_car', 'detail', 'time_in', 'home',
                'guard', 'time_guard', 'time_user', 'guard_check', 'status_guard',
                'status_user', 'status_home', 'code_status', 'active_sleep', 'village',
                'color_car', 'brand_car')

    def create(self, validated_data):
        guard = validated_data.pop("guard")
        code_scan = CodeScan.objects.create(**validated_data)
        for g in guard:
            code_scan.guard.add(g)
        code_scan.save()
        return code_scan