from odoo import http
class Academy(http.Controller):
    # có thể tạo 1 list các đường dẫn khác nhau cùng trỏ vào 1 page bằng việc cho vào list
    # phân quyền auth: 'public' | 'user' | 'admin' : với user hoặc user là admin thì phải login mới truy cập được
    @http.route(['/academy/academy/', '/viindoo/'], auth='public', website=True)
    def index(self, **kw):
        Teachers=http.request.env['academy.teachers']
        # .index là id của file template được định nghĩa muốn sử dụng ở module thay thế
        return http.request.render('viindoo_academy.index',{'teachers':Teachers.sudo().search([])
            })
    
    # @http.route('/academy/<name>/', auth='public', website=True)
    # def teacher(self, name):
    #     return '<h1>{}</h1>'.format(name)
    
    # @http.route('/academy/<int:id>/', auth='public', website=True)
    # def teacher2(self, id):
    #     return '<h1>{} ({})</h1>'.format(id, type(id).__name__)
    #

    @http.route('/academy/<model("academy.teachers"):teacher>/', auth='public', website=True)
    def teacher3(self, teacher):
        # academy.biography: là 1 template
        return http.request.render('viindoo_academy.biography', {
        'person': teacher
    })