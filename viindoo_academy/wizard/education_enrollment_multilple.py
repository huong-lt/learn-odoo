from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WizardEnrollmentMultiple(models.TransientModel):
    _name = 'wizard.enrollment.multiple'
    _description = 'Multiple Enrollment Wizard'

    active_model = fields.Char()
    registration_number = fields.Char(required=True)
    class_ids = fields.Many2many('education.class', string='Class')
    student_ids = fields.Many2many('education.student', string = 'Students')
    date = fields.Date(string = "Enrollment Date", required=True)
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
    
        active_model = self._context.get('active_model')
        res['active_model'] = active_model
        res['date'] = fields.Date.today()
        return res
    
    def enroll_multiple(self):
        vals_list = []
        active_model = self.env.context.get('active_model')

        if active_model == 'education.class':
            class_ids = self.env[active_model].browse(self.env.context.get('active_ids'))
            student_ids = self.student_ids
        elif active_model == 'education.student':
            class_ids = self.class_ids
            student_ids = self.env[active_model].browse(self.env.context.get('active_ids'))
        for c in class_ids:
            for s in student_ids:
                vals = {
                    'name': self.registration_number,
                    'date': self.date,
                    'class_id': c.id,
                    'student_id': s.id               
                }
                vals_list.append(vals)
        self.env['education.enrollment'].create(vals_list)
        return
    
    