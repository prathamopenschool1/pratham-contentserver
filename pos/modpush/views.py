import os
import json
import logging
from django.db.models import query
from django.shortcuts import render
from django.views.generic import View
from .pushhelper.connectcheck import PushHelper
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import UsageData, DeskTopData,DbPushData


# This retrieves a Python logging instance (or creates it)
infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")


class PushDataView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'modpush/data_to_push.html')


class PushUsageDataView(View):

    psh = PushHelper()

    def post(self, request, *args, **kwargs):
        infoLogger.info("In push_usageData")
        infoLogger.info("internet connection status" +  str(self.psh.connect()))

        if self.psh.connect() == True:
            result_data = self.psh.push_usageData()
            if result_data['status'] == 403:
                context = {'msg': 'No Data'}
                context = json.dumps(context)
                return JsonResponse(context, safe=False)
            else:
                clear_usage_data()
                context = {'msg': 'success'}
                context = json.dumps(context)
                return JsonResponse(context, safe=False)

        else:
            return render(request, 'core/NoInternetFound.html')


#new method to clear UsageData model data just after pushing usage data zip from push_usageData
def clear_usage_data():
    instance_usage = UsageData.objects.all()
    instance_usage.delete()



class DbPushDataView(View):
    psh = PushHelper()

    def post(self, request, *args, **kwargs):
        infoLogger.info("In push_dbPushData")
        infoLogger.info("internet connection status" +  str(self.psh.connect()))
        if self.psh.connect() == True:
            result_data = self.psh.push_dbPushData()
            if result_data['status'] == 403:
                context = {'msg': 'No Data'}
                context = json.dumps(context)
                return JsonResponse(context, safe=False)
            else:
                clear_dbpush_data()
                context = {'msg': 'success'}
                context = json.dumps(context)
                return JsonResponse(context, safe=False)
        else:
            return render(request, 'core/NoInternetFound.html')


#new method to clear DbPushData model data just after pushing dbpush data zip from push_dbpushData
def clear_dbpush_data():
    instance_dbpush = DbPushData.objects.all()
    instance_dbpush.delete()



class DeskTopDataToServerView(View):
    psh = PushHelper()

    def post(self, request, *args, **kwargs):
        infoLogger.info("Calling desktop_data_to_server")
        infoLogger.info("internet connection status" +  str(self.psh.connect()))
        if self.psh.connect() == True:
            result_data = self.psh.desktop_data_to_server()
            if result_data['status'] == 404 or result_data['status'] == 403:
                context = {'msg': 'No Data'}
                context = json.dumps(context)
                return JsonResponse(context, safe=False)
            elif result_data['status'] == 203:
                clear_desktop_data()
                desktop_data = json.dumps(result_data)
                return render(request, 'modpush/showPushedDTData.html', context={"desktop_data": desktop_data})
            else:
                clear_desktop_data()
                context = {'msg': 'success'}
                context = json.dumps(context)
                return JsonResponse(context, safe=False)

        else:
            return render(request, 'core/NoInternetFound.html')


#new method to clear desktop model data just after pushing desktop data to pos server
def clear_desktop_data():
    instance_desktop = DeskTopData.objects.all()
    instance_desktop.delete()


class BackUpDataView(View):

    psh = PushHelper()

    def post(self, request, *args, **kwargs):
        result_data = self.psh.backup()
        if result_data['status'] == 404 or result_data['status'] == 403:
            context = {'msg': 'No Data'}
            context = json.dumps(context)
            return JsonResponse(context, safe=False)
        else:
            context = {'msg': 'success'}
            context = json.dumps(context)
            return JsonResponse(context, safe=False)


class ClearDataView(View):

    psh = PushHelper()

    def post(self, request, *args, **kwargs):

        queryset_usage = UsageData.objects.all()
        queryset_dbpush = DbPushData.objects.all()
        queryset_desktop = DeskTopData.objects.all()

        if not queryset_usage and not queryset_dbpush and not queryset_desktop:
            self.psh.deleteUsageZipFiles()
            self.psh.deleteDbPushZipFiles()
            context = {'msg': 204}
            context = json.dumps(context)
            return JsonResponse(context, safe=False)
        else:
            queryset_usage.delete()
            queryset_dbpush.delete()
            queryset_desktop.delete()
            self.psh.deleteUsageZipFiles()
            self.psh.deleteDbPushZipFiles()
            context = {'msg': 'success'}
            context = json.dumps(context)
            return JsonResponse(context, safe=False)