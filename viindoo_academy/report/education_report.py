from odoo import models, fields, api


class EducationReport(models.Model):
    _name = 'education.report'
    _description = "Education Report"
    _auto = False
    class_id = fields.Many2one('education.class', string='Class', readonly=True)
    student_id = fields.Many2one('education.student', string='Student', readonly=True)
    enrollment_date = fields.Date(readonly=True, string="Enrollment Date")
    course_id = fields.Many2one('education.course', string='Course', readonly=True)
    country_id = fields.Many2one('res.country', string="Country")
    responsible_id = fields.Many2one('res.users', string='Responsible', readonly=True)
    ref=fields.Text(readonly=True, string='Ref.')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ], string='Class Status', readonly=True)
    
    @property
    def _table_query(self):
        res = '%s %s %s %s' % (self._select(), self._from(), self._where(), self._group_by())
        return res
 
    @api.model
    def _select(self):
        return """
        SELECT 
        course.id as course_id, 
        course.name,
        cls.name,
        cls.state,
        cls.responsible_id,
        enroll.id, 
        enroll.name as ref,
        enroll.class_id,  
        enroll.student_id, 
        enroll.date as enrollment_date
        """
        
    @api.model
    def _from(self):
        return """
        FROM 
        education_enrollment enroll 
        join education_class cls on cls.id=enroll.class_id
        join education_student student on student.id=enroll.student_id
        join education_course course on course.id=cls.course_id
        """
        
    @api.model
    def _where(self):
        return """
        
        """

    @api.model
    def _group_by(self):
        return """
        
        """    
        
             
