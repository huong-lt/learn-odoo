from odoo import models, fields, api
from datetime import date
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
        today=date.today()
        for r in self:
            r.age = today.year-r.birthday.year 