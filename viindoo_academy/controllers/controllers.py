from odoo import http
class Academy(http.Controller):
    # có thể tạo 1 list các đường dẫn khác nhau cùng trỏ vào 1 page bằng việc cho vào list
    # phân quyền auth: 'public' | 'user' | 'admin' : với user hoặc user là admin thì phải login mới truy cập được
    @http.route(['/viindoo_academy/academy/', '/viindoo/'], auth='public', website=True)
    def index(self, **kw):
        Teachers=http.request.env['academy.teachers']
        # .index là id của file template được định nghĩa muốn sử dụng
        return http.request.render('viindoo_academy.index',{'teachers':Teachers.sudo().search([])
            })