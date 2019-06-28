"""TCSDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,re_path
from . import views
from . import api

urlpatterns = [
    re_path(r'^api/dut/add/$', api.AddDUTNodes.as_view()),
    re_path(r'^api/dut/change_fw/$', api.ChangeDUTFW.as_view()),
    re_path(r'^api/dut/change_host/$', api.ChangeDUTHost.as_view()),
    re_path(r'^api/dut/change_info/$', api.ChangeDUTBasicInfo.as_view()),
    re_path(r'^api/dut/add_monitor/$', api.AddDUTMonitorRec.as_view()),
    re_path(r'^api/dut/get_info/$', api.GetDUTBasicInfo.as_view()),
    re_path(r'^api/dut/get_monitor/$', api.GetDUTHealthInfo.as_view()),
    re_path(r'^api/dut/get_by_host/$', api.GetAllDUTByHostName.as_view()),
    re_path(r'^api/dut/get_by_grp/$', api.GetAllDUTByGroupID.as_view()),
    re_path(r'^api/dut/get_by_tag/$', api.GetAllDUTByTag.as_view()),
    re_path(r'^api/dut/find/$', api.FindDuts.as_view()),
    re_path(r'^api/dut/change_grp/$', api.ChangeDUTGroupID.as_view()),
    re_path(r'^api/dut/change_tag/$', api.ChangeDUTTags.as_view()),
    re_path(r'^api/dut/change_status/$', api.ChangeDUTStatus.as_view()),
    re_path(r'^api/dut/get_status/$', api.GetDUTStatus.as_view()),
    re_path(r'^api/dut/get_tag/$', api.GetDUTTags.as_view()),
    re_path(r'^api/dut/get_grp/$', api.GetDUTGroupID.as_view()),

    re_path(r'^api/host/add/$', api.AddHostInfo.as_view()),
    re_path(r'^api/host/change_hw/$', api.ChangeHostHWInfo.as_view()),
    re_path(r'^api/host/change_net/$', api.ChangeHostNetInfo.as_view()),
    re_path(r'^api/host/change_slot/$', api.ChangeSlotDUTInfo.as_view()),
    re_path(r'^api/host/change_os/$', api.ChangeHostOSInfo.as_view()),
    re_path(r'^api/host/change_driver/$', api.ChangeHostDriverInfo.as_view()),
    re_path(r'^api/host/change_info/$', api.ChangeHostBasicInfo.as_view()),
    re_path(r'^api/host/add_monitor/$', api.AddHostMonitorRec.as_view()),
    re_path(r'^api/host/change_sw/$', api.ChangeHostSWInfo.as_view()),
    re_path(r'^api/host/get_info/$', api.GetHostBasicInfo.as_view()),
    re_path(r'^api/host/get_hw/$', api.GetHostHWInfo.as_view()),
    re_path(r'^api/host/get_net/$', api.GetHostNetInfo.as_view()),
    re_path(r'^api/host/get_os/$', api.GetHostOSInfo.as_view()),
    re_path(r'^api/host/get_driver/$', api.GetHostDriverInfo.as_view()),
    re_path(r'^api/host/get_sw/$', api.GetHostToolsInfo.as_view()),
    re_path(r'^api/host/get_monitor/$', api.GetHostCurStatus.as_view()),
    re_path(r'^api/host/get_slots/$', api.GetAllSlotsByHostName.as_view()),
    re_path(r'^api/host/find/$', api.FindHosts.as_view()),
    re_path(r'^api/host/disconnections/$', api.GetDisconnectedHost.as_view()),
    re_path(r'^api/host/get_status/$', api.GetHostStatus.as_view()),
    re_path(r'^api/host/change_status/$', api.ChangHostStatus.as_view()),

    re_path(r'^api/srt/add_pkg/$',api.AddSrtPkg.as_view()),
    re_path(r'^api/srt/add_srtinfo/$',api.AddSrtInfo.as_view()),
    re_path(r'^api/srt/chg_lab/$',api.ChgSrtPkgLabels.as_view()),
    re_path(r'^api/srt/get_pkg/$',api.GetSrtPkg.as_view()),
    re_path(r'^api/srt/get_srts/$',api.GetPkgSrtList.as_view()),
    re_path(r'^api/srt/find_pkg/$',api.FindSrtPkg.as_view()),

    re_path(r'^api/bin/add_pkg/$',api.AddFWPkg.as_view()),
    re_path(r'^api/bin/add_bin/$',api.AddFWBin.as_view()),
    re_path(r'^api/bin/add_rel/$',api.AddFWRel.as_view()),
    re_path(r'^api/bin/chg_lab/$',api.ChgFWPkgLabels.as_view()),
    re_path(r'^api/bin/get_bins/$',api.GetFWBins.as_view()),
    re_path(r'^api/bin/get_pkgs/$',api.GetFWPackes.as_view()),
    re_path(r'^api/bin/get_rels/$',api.GetFWRels.as_view()),
    re_path(r'^api/bin/find_pkg/$',api.FindFWPkgList.as_view()),
    re_path(r'^api/bin/find_rel/$',api.FindFWRelList.as_view()),

    re_path(r'^duts$', views.duts),
    re_path(r'^dut_update$', views.dut_update),
    re_path(r'^hosts$', views.hosts),
    re_path(r'^host_update', views.host_update),
    re_path(r'^asset_detail', views.asset_detail),
    re_path(r'^dut_record', views.dut_record),
    re_path(r'^host_record', views.host_record),
    re_path(r'^os_record', views.os_record),

    re_path(r'^package_list$', views.package_list),
    re_path(r'^package_add$', views.add_package),
    re_path(r'^package_update$', views.update_package),
    re_path(r'^package_del$', views.del_package),
    re_path(r'^script_list/(?P<pid>\d*)/$', views.script_list),
    re_path(r'^script_add$', views.add_script),
    re_path(r'^script_update$', views.update_script),
    re_path(r'^script_del$', views.del_script),


]
