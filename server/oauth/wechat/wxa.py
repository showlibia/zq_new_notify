from wechatpy import WeChatClientException
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from server.oauth.wechat import wechat_client
from rest_framework.response import Response
def get_openid(code:str):
    try:
        openid = wechat_client.wxa.code_to_session(code)["openid"]
        return Response({'openid': openid})
    except WeChatClientException as e:
        if e.errcode == 40029:
            raise APIException(detail="微信登录失败，请重新登录", code=HTTP_400_BAD_REQUEST)
        raise APIException(detail=f"微信登录失败 [{e.errcode}] {e.errmsg}", code=HTTP_500_INTERNAL_SERVER_ERROR)
def get_user_phone_num(code:str):

    try:
        data = {"code": code}
        result = wechat_client.wxa._post("wxa/getuserphonenumber", data=data)
        phone_info = result["phone_info"]
        if phone_info["countryCode"] != "86":
            raise APIException(detail="仅支持中国大陆手机号", code=HTTP_400_BAD_REQUEST)
        return Response({'phone_number': phone_info["purePhoneNumber"]})
    except WeChatClientException as e:
        raise APIException(detail=f"获取用户手机号失败 [{e.errcode}] {e.errmsg}", code=HTTP_500_INTERNAL_SERVER_ERROR)