
from celery_tasks.main import app

@app.task
def ccp_send_sms_code(mobile, sms_code):

    from libs.yuntongxun.sms import CCP
    ccp = CCP()
    send_result = ccp.send_template_sms(mobile, [sms_code, 5], 1)
    return send_result

