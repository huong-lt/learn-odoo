from odoo import models, fields, api
from odoo.exceptions import UserError


class EducationClass(models.Model):
    _name = 'education.class'
    _description = 'Education Class'
    
    name = fields.Char(
        string='Name',
        help="The name of the class for identification",
        required=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
            ],
        string='Status',
        default='draft',
        help="Status of the class",
        )
    description = fields.Text(
        string='Description',
        help="The description for identification."
        )    
    active = fields.Boolean(default=True)
    
    start_date = fields.Date(
        string='Start Date',
        help="The date from of class",
        )
    end_date = fields.Date(
        string='End Date',
        help="The date of class",
        )    
    student_ids = fields.One2many(
        comodel_name='education.student',
        inverse_name='class_id',
        string='Students',
        help="The students that belong to the class."
        )
    
    enroll_ids = fields.One2many('education.enrollment','class_id')
    enroll_students_ids=fields.Many2many(
        comodel_name='education.student', 
        relation='enroll_student_rel',
        column1='class_id',
        column2='student_id',
        compute='_compute_enrolled_student_ids',
        store=True)
    
    course_id = fields.Many2one(        
        comodel_name='education.course',
        string='Course', 
        required=True,
        help="The Course of class"
        )
    historical_student_ids = fields.Many2many(
        comodel_name='education.student',
        relation='class_education_rel',
        column1='class_id',
        column2='student_id',
        string="Historical Students"
        )
    students_count = fields.Integer(
        string='Students Count', 
        compute='_compute_students_count', 
        store=True
        )
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    responsible_id = fields.Many2one('res.users', string='Responsible', store=True)

    _sql_constraints = [('class_name_unique','unique(name)',"The name of Class must be unique")]

    @api.depends('enroll_ids')
    def _compute_students_count(self):
        for r in self:
            r.students_count = len(r.enroll_ids)
            
    @api.depends('enroll_ids.student_id')
    def _compute_enrolled_student_ids(self):
        for r in self:
            r.enroll_students_ids = r.enroll_ids.student_id 

    @api.constrains('start_date','end_date')
    def _check_dates(self):
        for r in self:
            if r.start_date and r.end_date and r.start_date > r.end_date:
                raise UserError("The start date must NOT be later than the end date")

   
    
    
    
    

