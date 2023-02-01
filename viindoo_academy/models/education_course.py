from odoo import models, fields, api


class EducationCourse(models.Model):
    _name = 'education.course'
    _description = 'Courses'
    
    name = fields.Char(
        string='Course Name',
        required=True
        )

    description = fields.Text(
        string='Description',
        )
    class_ids = fields.One2many(
        comodel_name='education.class',
        inverse_name='course_id',
        string='Class',
        help="The class that belong to the course.")
    
    class_count = fields.Integer(string='Class Count', compute='_get_class', readonly=True, default=0)
    students_count = fields.Integer(string='Student Count', compute='_get_students', readonly=True, default=0)
    _sql_constraints = [('course_name_unique', 'unique(name)', "The name of Course must be unique!")]
    
    @api.depends('class_ids')
    def _get_class(self):
        for r in self:
            r.class_count = len(r.class_ids)
    
    @api.depends('class_ids')
    def _get_students(self):
        students_list=[]
        for r in self:
            if r.class_ids:
                for c in r.class_ids.enroll_ids:
                    if c.student_id not in students_list:
                        students_list.append(c.student_id )
                    
            r.students_count=len(students_list)        
            # r.students_count = len(students_list)
            # self.env.cr.execute("""
            #     select count(s.name )
            #     from education_student s join education_enrollment e
            #     on s.id=e.student_id
            #     join education_class c
            #     on e.class_id=c.id
            #     join education_course r on c.course_id=r.id
            #     where r.id= %s
            # """, 4)
          
                
    def action_view_class(self):
        result = self.env['ir.actions.act_window']._for_xml_id('viindoo_academy.education_class_action')
        class_count = len(self.class_ids)
        if class_count != 1:
            result['domain'] = "[('id', 'in', %s)]" % self.class_ids.ids
        elif class_count == 1:
            res = self.env.ref('viindoo_academy.education_class_view_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.class_ids.id
        return result
    
    def action_view_students(self):
        students_list=[]
        for r in self:
            if r.class_ids:
                for c in r.class_ids.enroll_ids:
                    students_list.append(c.student_id.id)
        result = self.env['ir.actions.act_window']._for_xml_id('viindoo_academy.education_student_action')
        students_count = len(students_list)
        if students_count != 1:
            result['domain'] = "[('id', 'in', %s)]" % students_list
        elif students_count == 1:
            res = self.env.ref('viindoo_academy.education_student_view_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.class_ids.enroll_ids.student_id.id
        return result
