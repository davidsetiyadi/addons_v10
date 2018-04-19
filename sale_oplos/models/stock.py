# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.addons.procurement.models import procurement
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class StockMove(models.Model):
	_inherit = "stock.move"

	oplos_template_id = fields.Many2one('product.template', string='Oplos', change_default=True)

	@api.onchange('product_id')
	def onchange_product_id(self):
		product = self.product_id.with_context(lang=self.partner_id.lang or self.env.user.lang)
		self.name = product.partner_ref
		oplos_template_ids = False
		self.product_uom = product.uom_id.id
		self.product_uom_qty = 1.0
		for oplos in product.product_tmpl_id.sale_oplos_ids:	
			oplos_template_ids.append(oplos.id)

		return {'domain': {	'product_uom': [('category_id', '=', product.uom_id.category_id.id)],
							'oplos_template_id': [('id','in',oplos_template_ids)]}}

	@api.multi
	@api.onchange('oplos_template_id')
	def oplos_id_change(self):
		if not self.product_id:
			return False
		vals = {}
		# name = ''
		product = self.product_id.with_context(
			lang=self.order_id.partner_id.lang,
			partner=self.order_id.partner_id.id,
			quantity=self.product_uom_qty,
			date=self.order_id.date_order,
			pricelist=self.order_id.pricelist_id.id,
			uom=self.product_uom.id
		)
		name = product.name_get()[0][1]
		# vals['name'] = name
		if self.oplos_template_id:
			vals['name'] = self.oplos_template_id.name_get()[0][1]
		
		
		self.update(vals)