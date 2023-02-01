from odoo import models, fields, api


class EducationStudent(models.Model):
    _name = 'education.student'
    _description = ' Education Student'
    
    name = fields.Char(
        string='Name',
        required=True)
    class_id = fields.Many2one(
        comodel_name='education.class',
        string='Class', help="The Class of student")
    
    
    class_ids = fields.Many2many(
        comodel_name='education.class',
        relation='class_education_rel',
        column1='student_id',
        column2='class_id',
        string='Enrolled Classes')

    ethnic_id = fields.Many2one('res.ethnic')
    ethnic_code = fields.Char(related='ethnic_id.code', store=True)
    
    ethnic_code2 = fields.Char(compute='_compute_ethnic_code2', store=True)
    user_id = fields.Many2one('res.users', string='Student', store=True)
    
    enrollment_ids=fields.One2many('education.enrollment','student_id')
    
    class_count = fields.Integer(
        string='Class Count', 
        compute='_compute_class_count', 
        store=True
        )
    @api.depends('ethnic_id')
    def _compute_ethnic_code2(self):
        for r in self:
            r.ethnic_code2 = r.ethnic_id.code
            
    @api.onchange('ethnic_id')
    def _onchange_country(self):
        self.country_id = self.ethnic_id.country_ids[-1:]
        
    @api.depends("user_id")
    def _compute_name(self):
        for r in self:
            r.name = r.user_id.name
            
    @api.depends('enrollment_ids')
    def _compute_class_count(self):
        for r in self:
            r.class_count = len(r.enrollment_ids)       
            