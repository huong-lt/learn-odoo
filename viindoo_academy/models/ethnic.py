from odoo import models, fields, api


class ResEthnic(models.Model):
    _name = 'res.ethnic'
    _description = 'Ethnic'
    
    name = fields.Char(
        string='Name',
        help="The name of nation",
        required=True)

    code = fields.Char(
        string='Code',
        required=True,
        # groups='base.group_user,base.group_portal'
        )
    

