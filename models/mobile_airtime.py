# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import relativedelta
from odoo import fields, models, api
from odoo.exceptions import ValidationError



class MobileAirtimeAdvance(models.Model):
    _name = 'mobile.airtime'
    _description = "Mobile Airtime"
    _inherit = ["mail.thread"]
    _order = "id desc"

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
    same_user = fields.Boolean(compute='check_login_user')
    date_added = fields.Datetime('Date Requested')
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
    currency_id = fields.Many2one(
        related='employee_id.company_id.currency_id',
        track_visibility='onchange')
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
    @api.multi
    def advance_approval(self):
        """ sets the draft airtime  request to waiting approval"""
        for record in self:
            if not record.employee_id:
                raise ValidationError('Missing Employee record')
            elif not record.employee_id.parent_id:
                raise ValidationError(
                    'Your manager is not added in your HR records,\
                            no one to approve your Airtime request')
            elif not record.employee_id.parent_id.user_id:
                raise ValidationError(
                    'Your manager does have access to the accounts system to \
                            approve your Airtime request. Please consult acconts')
            else:
                # record.message_subscribe_users(
                #     user_ids=[record.employee_id.parent_id.user_id.id])
                return record.write({'state': 'approval'})

    @api.multi
    def advance_approved(self):
        """ approves a airtime  request """
        for record in self:
            record.write({'state': 'approved'})

    @api.multi
    def advance_disapproved(self):
        """ disapproves a salary advance request """
        for record in self:
            record.write({'state': 'disapproved'})

    @api.multi
    def advance_reset(self):
        """ resets a airtime  request currently waiting approval"""
        for record in self:
            record.write({'state': 'draft'})
