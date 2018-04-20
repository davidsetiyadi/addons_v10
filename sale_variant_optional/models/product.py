# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import itertools
import psycopg2

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError,ValidationError, except_orm


class ProductTemplate(models.Model):
	_inherit = "product.template"

	@api.multi
	def write(self, vals):
		res = super(ProductTemplate, self).write(vals)
		types = []
		for template in self:
			for attribute in template.attribute_line_ids:
				if attribute.type_variant in types:
					raise UserError(_('Sorry, You can\'t use the same type in same product.'))
				else:
					types.append(attribute.type_variant)
					
		return res

	@api.model
	def create(self, vals):
		# TDE FIXME: context brol		
		template = super(ProductTemplate, self).create(vals)
		types = []
		for attribute in template.attribute_line_ids:
			if attribute.type_variant in types:
				raise UserError(_('Sorry, You can\'t use the same type in same product.'))
			else:
				types.append(attribute.type_variant)
		return template

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def name_get(self):
        # TDE: this could be cleaned a bit I think

        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            if code:
                name = '[%s] %s' % (code,name)
            return (d['id'], name)

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []
        for product in self.sudo():
            # display only the attributes with multiple possible values on the template
            variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id')
            variant = product.attribute_value_ids._variant_name(variable_attributes)
            name = variant and "%s (%s)" % (product.name, variant) or product.name
            # name = product.name
            sellers = []
            if partner_ids:
                sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and (x.product_id == product)]
                if not sellers:
                    sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and not x.product_id]
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result