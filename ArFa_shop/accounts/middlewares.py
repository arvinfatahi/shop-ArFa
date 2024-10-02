# accounts/middlewares.py
from django.contrib.sessions.middleware import SessionMiddleware

class SeparateAdminSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        # بررسی کنید که آیا درخواست برای پنل ادمین است
        if request.path.startswith('/admin/'):
            # استفاده از کوکی مخصوص پنل ادمین
            request.session_key = request.COOKIES.get('admin_sessionid')
        else:
            # استفاده از کوکی برای سایت اصلی
            request.session_key = request.COOKIES.get('sessionid')

    def process_response(self, request, response):
        if request.path.startswith('/admin/'):
            # تنظیم کوکی برای پنل ادمین
            response.set_cookie('admin_sessionid', request.session.session_key)
        else:
            # تنظیم کوکی برای سایت اصلی
            response.set_cookie('sessionid', request.session.session_key)
        return response
