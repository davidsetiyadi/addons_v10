# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class dev_41_surat_pengantar_barang_citi(models.Model):
#     _name = 'dev_41_surat_pengantar_barang_citi.dev_41_surat_pengantar_barang_citi'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100