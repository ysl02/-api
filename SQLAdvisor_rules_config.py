from OpsManage.Utils.api_util import api_request_util
from OpsManage.models import SQLAdvisor_rule_config
from OpsManage.Utils.JsonResponse import JsonResponse
from django.db.models import Q
from OpsManage.serializers import SQLAdvisor_rule_configSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from OpsManage.settings import LOCAL_SERVER_URL


class RuleView(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SQLAdvisor_rule_config.objects.filter()
    serializer_class = SQLAdvisor_rule_configSerializer

    def __init__(self):
        self.return_dict = {}

    def get_objects(self, request):
        try:
            keyword = request.data.get("Args").get("id")
            return self.get_queryset().get(pk=keyword)
        except Exception as e:
            return JsonResponse(message=str(e))

    def get_keyword(self, request):
        try:
            keyword = request.data.get("Args").get("keyword", "")
            return keyword
        except Exception as e:
            return JsonResponse(message=str(e))

    def RuleListView(self, request):
        keyword = self.get_keyword(request)
        if keyword:
            queryset2 = self.get_queryset().filter(
                Q(rule_name__icontains=keyword)
                | Q(rule_desc__icontains=keyword))
        else:
            queryset2 = self.get_queryset()
        self.return_dict['rows'] = self.get_serializer(instance=queryset2, many=True).data
        return JsonResponse(success=True, data=self.return_dict, message='获取成功')

    def RuleUpdateView(self, request):
        args = request.data.get("Args")
        url = LOCAL_SERVER_URL + "/api/set_sqladvisor_variables_api/"
        result = api_request_util('1', url, "POST", args)

        if result["Success"]:
            instance = self.get_objects(request)
            serializer = self.get_serializer(instance=instance, data=request.data.get("Args"))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(success=True, data=serializer.data, message='修改成功')
        return JsonResponse(success=False, data=result.data["Data"], message=result.data["Message"])
