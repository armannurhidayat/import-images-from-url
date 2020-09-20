from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import logging
_logger = logging.getLogger(__name__)
import time
from io import BytesIO
from collections import OrderedDict
import pytz
import xlsxwriter
import base64
from datetime import datetime
from pytz import timezone
import xlrd
from xlrd import open_workbook
import requests


class ImportImageProductWizard(models.TransientModel):
	_name = 'import.image.product.wizard'

	file_data	= fields.Binary(string='Import File')
	filename 	= fields.Char(string='File Name')


	@api.multi
	def action_import(self):
		try :
			if not self.file_data :
				raise Warning("Please select a file first.")
			wb = open_workbook(file_contents=base64.decodestring(self.file_data))
			values = []

			for s in wb.sheets():
				for row in range(s.nrows):
					col_value = []
					for col in range(s.ncols):
						value = (s.cell(row, col).value)
						col_value.append(value)
					values.append(col_value)

			product_product_obj = self.env['product.template']

			row = 1
			for data in values:
				if row != 1:
					product_name 	= data[0]
					standard_price	= data[1]
					default_code	= data[2]
					type			= data[3].lower()
					lst_price		= data[4]
					image_url		= data[5]
					# Convert base64
					response 		= requests.get(image_url)
					b64response 	= base64.b64encode(requests.get(image_url).content)

					product_name_exist 	= product_product_obj.search([('name','=',product_name)])

					if product_name_exist:
						product_name_exist.standard_price	= standard_price
						product_name_exist.default_code		= default_code
						product_name_exist.type 			= type
						product_name_exist.lst_price 		= lst_price
						product_name_exist.image_medium 	= b64response
					else:
						product_product_obj.create({
							'name'				: product_name,
							'standard_price'	: standard_price,
							'default_code'		: default_code,
							'type'				: type,
							'lst_price'			: lst_price,
							'image_medium'		: b64response,
						})


				row += 1

		except Exception as error :
			raise Warning(error)

		views = [(self.env.ref('product.product_template_kanban_view').id, 'kanban'), (self.env.ref('product.product_template_only_form_view').id, 'form')]
		return {
			'name'		: _('Products'),
			'domain'	: [],
			'view_type' : 'form',
			'res_model' : 'product.template',
			'context'	: {},
			'view_id'	: False,
			'views'		: views,
			'view_mode' : 'kanban,form',
			'type'		:'ir.actions.act_window',
		}