# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

logger = logging.getLogger(__name__)


class SupermarketProduct(models.Model):
    _name = 'supermarket.product'
    _description = 'supermarket product'

    name = fields.Char('Name', required=True)
    date_purch = fields.Date('Purchase Date')
    provider_ids = fields.Many2many('res.partner', string='Provider')
    category_id = fields.Many2one('supermarket.product.category', string='Category')

    state = fields.Selection([
        ('fresh', 'Available'),
        ('roten', 'Unavailable'),
        ('retired', 'Retired')],
        'State', default="fresh")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('fresh', 'roten'),
                   ('fresh', 'retired'),
                   ('roten', 'retired'),
                   ('retired', 'fresh')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for product in self:
            if product.is_allowed_transition(product.state, new_state):
                product.state = new_state
            else:
                message = _('Moving from %s to %s is not allowd') % (product.state, new_state)
                raise UserError(message)

    def make_available(self):
        self.change_state('fresh')

    def make_unavailable(self):
        self.change_state('roten')

    def make_retired(self):
        self.change_state('retired')

    def log_all_supermarket_members(self):
        supermarket_member_model = self.env['supermarket.member']  # This is an empty recordset of model supermarket.member
        all_members = supermarket_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True


    def create_categories(self):
        categ1 = {
            'name': 'Expired short',
            'description': 'Short expiration date'
        }
        categ2 = {
            'name': 'Expired medium',
            'description': 'Medium expiration date'
        }
        parent_category_val = {
            'name': 'Expired long',
            'description': 'Long expiration date',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        # Total 3 records (1 parent and 2 child) will be craeted in supermarket.product.category model
        record = self.env['supermarket.product.category'].create(parent_category_val)
        return True

    def change_purchase_date(self):
        self.ensure_one()
        self.date_purch = fields.Date.today()
        self.date_expiration = fields.Date.today()

    def find_product(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'Product Name'),
                     ('category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'Product Name 2'),
                     ('category_id.name', '=', 'Category Name 2')
        ]
        products = self.search(domain)
        logger.info('products found: %s', products)
        return True

class supermarketMember(models.Model):

    _name = 'supermarket.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "supermarket member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    provided_products_ids = fields.Many2many(
        'supermarket.product',
        string='Provided products'
        #, relation='supermarket_product_res_partner_rel'  # optional
    )