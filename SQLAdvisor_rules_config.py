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
    
    def api_request_util(user_id, url, request_method, param=None):
    token = Token.objects.get(user_id=user_id)
    headers = {"Authorization": "Token %s" % token}
    request_method = str(request_method).upper()

    try:
        if request_method == 'GET':
            response = requests.get(url, params=param, headers=headers, verify=False)
        elif request_method == 'POST':
            headers["Content-Type"] = "application/json"
            response = requests.post(url, json=param, headers=headers, timeout=3600, verify=False)
        else:
            return {"msg": "request method is not supported"}
        return json.loads(response.text)
    except Exception as e:
        return {"msg": str(e)}

    def RuleUpdateView(self, request):
        args = request.data.get("Args")
        url = LOCAL_SERVER_URL + "/api/set_sqladvisor_variables_api/"
        result = api_request_util('1', url, "POST", args)
        
        LOCAL_SERVER_URL = "http://192.168.56.102:8000"

        if result["Success"]:
            instance = self.get_objects(request)
            serializer = self.get_serializer(instance=instance, data=request.data.get("Args"))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(success=True, data=serializer.data, message='修改成功')
        return JsonResponse(success=False, data=result.data["Data"], message=result.data["Message"])
    
