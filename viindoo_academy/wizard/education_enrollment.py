from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WizardEnrollmentSingle(models.TransientModel):
    _name = 'wizard.enrollment.single'
    _description = 'Single Enrollment Wizard'
    
    registration_number = fields.Char(required=True)
    class_id = fields.Many2one('education.class', string='Class', required=True)
    student_id = fields.Many2one('education.student', string='Student', required=True)
    date = fields.Date(
        help="The date on which the student enrolls"
        )
    
    active_model = fields.Char()
    wizard_multi_id=fields.Many2one('wizard.enrollment.multi')
    
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        
        active_model = self._context.get('active_model')
        active_id = self._context.get('active_id')

        if active_model == 'education.class':
            res['class_id'] = active_id
        elif active_model == 'education.student':
            res['student_id'] = active_id
        res['active_model'] = self._context.get('active_model')
        res['date'] = fields.Date.today()
        return res
    
    def enroll(self):

        if not self.class_id or not self.student_id:
            raise UserError(_("You must specify both class and student fist."))
        # if  self.class_id.state !='confirmed':
        #             raise UserError(_("You cannot enroll in the class %s because the class status is not confirmed!"%self.class_id.name)) 
        self.env['education.enrollment'].create({
            'name': self.registration_number,
            'class_id': self.class_id.id,
            'student_id': self.student_id.id,
            'date': self.date or fields.Date.today()
            })
        
class WizardEnrollmentMutil(models.TransientModel):
    _name='wizard.enrollment.multi'
    
    line_ids=fields.One2many('wizard.enrollment.single','wizard_multi_id')
    
    def enroll2(self):
        active_ids=self._context.get('active_ids')
        active_model=self._context.get('active_model')
        for c in active_ids:
            for l in self.line_ids:
                if active_model == 'education.class':
                    l.class_id=c
                elif active_model == 'education.student':
                    l.student_id=c
                l.enroll()
        
    def enroll(self):
        vals_list=[]
        active_model=self._context.get('active_model')
        records=self.env[active_model].browse(self.env.context.get('active_ids'))
        for record in records:
            for line in self.line_ids:
                # if active_model=='education.class' and line.class_id.state !='confirmed':
                #     raise UserError(_("You cannot enroll in the class %s because the class status is not confirmed!" %line.class_id.name)) 
                vals_list.append({
                    'name':line.registration_number,
                    'class_id':record.id if active_model=='education.class' else line.class_id.id,
                    'student_id':record.id if active_model=='education.student' else line.student_id.id,
                    'date':line.date or fields.Date.today()
                  })
        self.env['education.enrollment'].create(vals_list)        
        
        
        
        