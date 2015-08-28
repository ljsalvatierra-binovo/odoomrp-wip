# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Mrp Bom Sale Pack",
    "version": "1.0",
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "website": "www.odoomrp.com",
    "category": "Sales Management",
    "contributors": ["Esther Martín <esthermartin@avanzosc.es>",
                     "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
                     "Ana Juaristi <anajuaristi@avanzosc.es>",
                     "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>"],
    "depends": ["base", "sale", "mrp", "sale_product_variants"],
    "data": ["views/mrp_bom_sale_pack_view.xml",
             "views/sale_order_mrp_view.xml"],
    "installable": True
}
