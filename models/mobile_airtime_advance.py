# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import relativedelta
from odoo import fields, models,api
from odoo.exceptions import ValidationError
LOGGER = logging.getLogger(__name__)

class MobileAirtimeAdvance(models.Model):
    _name = 'mobile.airtime' 
    -description = "Mobile Airtime Advance"
    -inherit=["mail.thread"]
    -order="id desc"
     @api.multi
    def _employee_get(self):
        return self.employee_id.search(
            [('user_id', '=', self.env.user.id)], limit=1).id

    @api.multi
    def check_login_user(self):
        """ set boolean value based on login user """
        for record in self:
            record.same_user = bool(record.env.user.id == record.user_id.id)

    name = fields.Char(
        'Request details',
        required=True,
        readonly=True,
        track_visibility='onchange',
        states={
            'draft': [
                ('readonly',
                 False)]})
    dept_id = fields.Many2one(
        'hr.department',
        'Department',
        track_visibility='always',
        related='employee_id.department_id')

       employee_id = fields.Many2one(
        'hr.employee',
        'Employee Name',
        default=_employee_get,
        required=True,
        track_visibility='always',
        readonly=True,
        states={
            'draft': [
                ('readonly',
                 False)]})
    user_id = fields.Many2one(
        'res.users',
        related='employee_id.user_id',
        track_visibility='always')
    state = fields.Selection([('draft',
                               'Draft'),
                              ('approval',
                               'Waiting Approval'),
                              ('approved',
                               'Approved'),
                              ('disapproved',
                               'Dis-approved')],
                             'Status',
                             default='draft', track_visibility='onchange')
    amount = fields.Monetary(
        'Amount',
        currency_field='currency_id',
        track_visibility='onchange', readonly=True, states={
            'draft': [
                ('readonly',
                 False)]})
    description = fields.Html(
        'Reasons for Request',
        readonly=True,
        states={
            'draft': [
                ('readonly',
                 False)]}, track_visibility='onchange')
date_added = fields.Datetime('Date Requested',default=lambda self: fields.Datetime.now(),) 
 same_user = fields.Boolean(compute='check_login_user')

    currency_id = fields.Many2one(
        related='employee_id.company_id.currency_id',
        track_visibility='onchange')
#   @api.multi
#     def advance_approval(self):
#         """ sets the draft salary advance request to waiting approval"""
#         for record in self:
#             if not record.employee_id:
#                 raise ValidationError('Missing Employee record')
#             elif not record.employee_id.parent_id:
#                 raise ValidationError(
#                     'Your manager is not added in your HR records,\
#                             no one to approve your salary advance request.Please co$
#             elif not record.employee_id.parent_id.user_id:
#                 raise ValidationError(
#                     'Your manager does have access to the HR system to \
#                             approve your salary advance request. Please consult HR')
#             else:
#                 record.message_subscribe_users(
#                     user_ids=[record.employee_id.parent_id.user_id.id])
#          @api.multi
#     def advance_approved(self):
#         """ approves a salary advance request """
#         for record in self:
#             deduction_type = self.env.ref('hr_ke.ke_deduction2')
#             if not deduction_type:
#                 raise ValidationError(
#                     "No salary rule found for processing salary advance in your pay$
#             values = {
#                 'employee_id': record.employee_id.id,
#                 'computation': 'fixed',
#                 'deduction_id': deduction_type.id,
#                 'rule_id': deduction_type.rule_id.id,
#                 'fixed': record.amount
#             }
#             if values:
#                 self.env['ke.deductions'].create(values)
#             else:
#                 raise ValidationError(
#                     'Missing Salary Advance details. Please consult payroll departm$
#             record.write({'state': 'approved'})

#         return record.write({'state': 'approval'})


