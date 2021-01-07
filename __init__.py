from  download_img import download_file

url = 'http://smarticle.video.ums.uc.cn/video/wemedia/e04efb1b26ca44a381f54cba58dfc222/96a9ae2f269539fd0eecff9f2bfce1ec-3746668663-2-0-2-h264.mp4?auth_key=1605855159-8e6b21c4011d46fbb639abb4d102ef53-0-81b53fca4c5cb5692a646f4d9dcd518e'
url = "https://iflow.uc.cn/webview/video?app=uc-iflow&aid=3096888451065448667&cid=622769673&zzd_from=uc-iflow&uc_param_str=dndsfrvesvntnwpfgicpbi&recoid=5759827539801271850&rd_type=reco&original_url=http%3A%2F%2Fv.ums.uc.cn%2Fvideo%2Fv_7cd346a8baeb5073.html&sp_gz=0&uc_biz_str=S%3Acustom%7CC%3Aiflow_video_hide&ums_id=7cd346a8baeb5073"
result = download_file(url, "", filename="a.mp4", call_func='')

print(result)