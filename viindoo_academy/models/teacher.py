from odoo import models, fields, api
class Teachers(models.Model):
    _name = 'academy.teachers'
    _decription="Teachers"

    name = fields.Char(
        string="Teacher"
        )
    birthday=fields.Date(
        string="Date of birth"
        )
    age = fields.Integer(
        string='Age', 
        compute='_compute_teacher_age'
        )
    biography=fields.Html()
    
    @api.depends('birthday')
    def _compute_teacher_age(self):
        today=fields.Date.today() # dùng thư viện của Odoo để có thể giả lập thời gian được
        for r in self:
            if r.birthday:
                r.age = today.year-r.birthday.year
            else:
                r.age=r.age 
                