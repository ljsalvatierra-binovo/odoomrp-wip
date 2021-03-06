# -*- coding: utf-8 -*-
# Copyright 2016 Daniel Campos - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class PreventiveOperationtype(models.Model):
    _name = 'preventive.operation.type'
    _description = 'Machinery preventive operation template type'

    name = fields.Char(string='Name')
    ref = fields.Char(string='Operation Reference')
    cycles = fields.Integer(string='Cycles')
    basedoncy = fields.Boolean(string='Based on Cycles')
    basedontime = fields.Boolean(string='Based on Time')
    margin_cy1 = fields.Integer(
        string='Cycles Margin 1', help="A negative number means that the"
        " alarm will be activated before the condition is met")
    margin_cy2 = fields.Integer('Cycles Margin 2')
    frequency = fields.Integer(string='Frequency',
                               help="Estimated time for the next operation.")
    interval_unit = fields.Selection(
        selection=[('day', 'Days'), ('week', 'Weeks'), ('mon', 'Months'),
                   ('year', 'Years')], string='Interval Unit')
    margin_fre1 = fields.Integer(
        string='Frequency Margin 1', help="A negative number means that the"
        " alarm will be activated before the compliance date")
    interval_unit1 = fields.Selection(
        selection=[('day', 'Days'), ('week', 'Weeks'), ('mon', 'Months'),
                   ('year', 'Years')], string='Interval Unit')
    margin_fre2 = fields.Integer(
        string='Frequency Margin 2', help="A negative number means that the"
        " alarm will be activated before the compliance date")
    interval_unit2 = fields.Selection(
        selection=[('day', 'Days'), ('week', 'Weeks'), ('mon', 'Months'),
                   ('year', 'Years')], string='Interval Unit')
    description = fields.Text('Description')
    hours_qty = fields.Float(string='Quantity Hours', required=False,
                             help="Expected time for the execution of the "
                             "operation. hh:mm")
    update_preventive = fields.Selection(
        selection=[('manual', 'Manual'),
                   ('before_repair', 'Before repair is done'),
                   ('after_repair', 'After repair is done')],
        string='Preventive Update', default="manual", required=True,
        help="Defines when the machine preventive operation will be"
        " recalcutated for next action. \n"
        "Manual => Last revision data should be changed manually.\n"
        "Before repair => Last revision data will be updated when repair is"
        " created.\n"
        "After repair => Last revision data will be updated when repair is"
        " done.")

    @api.constrains('basedoncy', 'cycles')
    def _check_basedoncy(self):
        for record in self:
            if record.basedoncy and record.cycles <= 0:
                raise ValidationError(
                    _("Operations based on cycles must have a positive cycle "
                      "frequency"))

    @api.constrains('basedontime', 'frequency', 'interval_unit')
    def _check_basedontime(self):
        for record in self:
            if record.basedontime and (
                    record.frequency <= 0 or not record.interval_unit):
                raise ValidationError(
                    _("Operations based on time must have a positive time "
                      "frequency"))

    @api.onchange('interval_unit')
    def _onchange_interval_unit(self):
        if self.interval_unit:
            self.interval_unit1 = self.interval_unit
            self.interval_unit2 = self.interval_unit

    @api.constrains('margin_cy1', 'margin_cy2')
    def _check_cycle_margins(self):
        for record in self:
            if record.margin_cy1 and record.margin_cy2 and (
                    record.margin_cy1 > record.margin_cy2):
                raise ValidationError(_('First margin must be before second'))

    @api.constrains('margin_fre1', 'interval_unit1', 'margin_fre2',
                    'interval_unit2')
    def _check_time_margins(self):
        for record in self:
            if record.interval_unit1 and record.interval_unit2:
                machine_operations = self.env['preventive.machine.operation']
                date = fields.Date.today()
                margin1 = machine_operations.get_interval_date(
                    date, record.margin_fre1, record.interval_unit1)
                margin2 = machine_operations.get_interval_date(
                    date, record.margin_fre2, record.interval_unit2)
                if margin1 > margin2:
                    raise ValidationError(
                        _("First margin must be before second"))


class PreventiveOperationMaterial(models.Model):
    _name = "preventive.operation.material"
    _description = "New material line."

    op_machi_mat = fields.Many2one(comodel_name='preventive.operation.matmach',
                                   string='Operation')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product', required=True)
    product_uom_qty = fields.Float(string='Quantity', default='1')
    product_uom = fields.Many2one(
        comodel_name='product.uom', string='Unit of Measure', required=True)

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.product_uom = self.product_id.uom_id.id


class PreventiveOperationMatmach(models.Model):
    # operation_machine_materials
    _name = 'preventive.operation.matmach'
    _description = 'Operation - Material - Machine Relation'

    name = fields.Char(string='Name')
    optype_id = fields.Many2one(comodel_name='preventive.operation.type',
                                string='Operation')
    opmaster = fields.Many2one(comodel_name='preventive.master',
                               string='Master Operation')
    material = fields.One2many(comodel_name='preventive.operation.material',
                               inverse_name='op_machi_mat', string='Material')
    basedoncy = fields.Boolean(related='optype_id.basedoncy')
    basedontime = fields.Boolean(related='optype_id.basedontime')
    cycles = fields.Integer(related='optype_id.cycles')
    frequency = fields.Integer(related='optype_id.frequency')
    interval_unit = fields.Selection(related='optype_id.interval_unit')
    update_preventive = fields.Selection(related='optype_id.update_preventive')
    hours_qty = fields.Float(related='optype_id.hours_qty')
    description = fields.Text(string='Description')

    @api.onchange('optype_id')
    def _onchange_optype_id(self):
        if self.optype_id:
            self.description = self.optype_id.description
