from odoo import models, fields, api
from odoo.exceptions import UserError


class HrLeaveType(models.Model):
    _inherit = "hr.leave.type"

    leave_validator_line_ids = fields.One2many('hr.leave.type.lines',
                                               "line_id")
    allocation_validation_type = fields.Selection(
        selection_add=[('multi', 'Multiple Approval')],
        ondelete={'multi': 'set default'})


class HrLeaveTypeLines(models.Model):
    _name = "hr.leave.type.lines"
    _description = "Hr Leave Type Lines"

    line_id = fields.Many2one("hr.leave.type")
    leave_validator_id = fields.Many2one("res.users",
                                         string="Approver")


class HrLeave(models.Model):
    _inherit = "hr.leave"

    approve_line_ids = fields.One2many('hr.leave.lines', "line_id")
    is_multi_approval = fields.Boolean("multi approval")
    is_approved = fields.Boolean("approved")
    approval_count = fields.Integer("count")

    # when change time off type  approvers are added if it is based on
    # multiple approval
    @api.onchange('holiday_status_id')
    def _onchange_holiday_status_id(self):
        vals = []
        if self.holiday_status_id.allocation_validation_type == 'multi':
            self.update({'is_multi_approval': True})
        else:
            self.update({'is_multi_approval': False})
        for line in self.holiday_status_id.leave_validator_line_ids:
            vals.append((0, 0, {
                    'approvers_id': line.leave_validator_id}))
        self.write({'approve_line_ids': [(5, 0)]})
        self.write({'approve_line_ids': vals})

    # button for  approval
    def action_multiapprovel(self):
        for line in self.approve_line_ids:
            if self.env.uid == line.approvers_id.id \
                    and line.status == 'to approve':
                line.update({'status': 'approved'})
                self.approval_count = self.approval_count+1
                if self.approval_count == len(self.approve_line_ids):
                    self.state = 'validate1'
                    self.is_approved = True


class HrLeaveLines(models.Model):
    _name = "hr.leave.lines"
    _description = "Hr Leave Lines"

    line_id = fields.Many2one("hr.leave")
    approvers_id = fields.Many2one("res.users", string="Approver",
                                   readonly=True)
    status = fields.Selection(string='Status', selection=[
        ('to approve', 'To Approve'),
        ('refuse', 'Refused'),
        ('approved', 'Approved')], default="to approve",  readonly=True)
    comment = fields.Char("Comment")

    # corresponding approver can change comments
    @api.onchange('comment')
    def _onchange_comment(self):
        if self.approvers_id.id != self.env.uid:
            raise UserError("Only The Approver Can Edit Comments")
