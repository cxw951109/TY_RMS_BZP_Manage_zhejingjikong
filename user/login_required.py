from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from Lib.Utils import *


class LoginRequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            if request.path[0:8] == '/static/' or request.path == '/warning/warning_numbers' or request.path[0:5] == '/api/' or request.path == '/drugTemplate/autoSearchDrugList/':
                return None
            print(request.path, 66666666666666)
            user = request.session['login_user']
            return None
        except Exception as e:
            print(e)
            if request.path == '/account/login/' or request.path == "/account/barcode/":
                return None
            else:
                visitType = request.GET.get('visitType')
                logger.info('用户没有登录, 跳转到登录页面')
                # if(((visitType=='1') or (visitType=='2'))):
                #     return redirect('/account/login?visitType=1')
                # else:
                #     return redirect('/account/login')
                if(visitType):
                    return redirect('/account/login?visitType='+visitType)
                else:
                    return redirect('/account/login')
