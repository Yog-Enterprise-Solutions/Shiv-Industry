# Copyright (c) 2024, YES and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class GatekeeperView(Document):
	def validate(self):
		return 0
		if not self.custom_purchase_receipt and len(self.items) > 0:
			i = 0
			def update_receipt(source,target, source_parent):
				# d = tuple(zip(self.items,target))			
				nonlocal i
							
				target.custom_quantity_received_by_gatekeeper = self.items[i].quantity_received_by_gatekeeper
				target.custom_item_image = self.items[i].item_image				
				frappe.log_error("SOURCE i",f"{self.items[i]}\ni: {i}")
				i += 1
			
			# images = 0
			# def update_images(source,target, source_parent):
			# 	nonlocal images
			# 	pass
			
			doc = get_mapped_doc(
				"Purchase Order",
				self.purchase_order,
				{
					"Purchase Order": {
						"doctype": "Purchase Receipt",
						"field_map": {"supplier_warehouse": "supplier_warehouse", "base_grand_total": "base_grand_total"},					
						"validation": {
							"docstatus": ["=", 1],
						},
					},
					"Purchase Order Item": {
						"doctype": "Purchase Receipt Item",
						"field_map": {
							"name": "purchase_order_item",
							"parent": "purchase_order",
							"bom": "bom",
							"material_request": "material_request",
							"material_request_item": "material_request_item",
							"sales_order": "sales_order",
							"sales_order_item": "sales_order_item",
							"wip_composite_asset": "wip_composite_asset",
						},				
						"postprocess": update_receipt,
						"condition": lambda doc: abs(doc.received_qty) < abs(doc.qty)
						and doc.delivered_by_supplier != 1,
					},				
					"Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges", "add_if_empty": True},
				}				
			)		
			# for image in self.images:
			for image in self.images:
				doc.append("custom_images", {
					"image": image.image,
					"description":image.description
				})
			doc.save()
			self.custom_purchase_receipt = doc.name
			# frappe.log_error("NEW NAME" , doc.name)			
			frappe.msgprint("Purchase Receipt created/mapped")
		else:
			if self.custom_purchase_receipt:
				pr = frappe.get_doc("Purchase Receipt", self.custom_purchase_receipt)
				common = self.images[:len(pr.custom_images)]			
				for i,item in enumerate(common):
					pr.custom_images[i].image= item.image
					pr.custom_images[i].description = item.description
				
				if len(self.images) > len(pr.custom_images):
					for image in self.images[len(pr.custom_images):]:
						pr.append("custom_images", {
							"image": image.image,
							"description":image.description
						})
				pr.save()

				common = self.items[:len(pr.items)]			
				for i,item in enumerate(common):
					pr.items[i].custom_quantity_received_by_gatekeeper= item.quantity_received_by_gatekeeper
					pr.items[i].custom_item_image = item.item_image
				
				if len(self.items) > len(pr.items):
					for item in self.items[len(pr.items):]:
						pr.append("items", {
							"custom_quantity_received_by_gatekeeper": item.quantity_received_by_gatekeeper,
							"custom_item_image":item.item_image
						})
				pr.save()

			else:
				pass

@frappe.whitelist()
def get_fields(purchase_order, name):	
	items= frappe.get_doc("Purchase Order", purchase_order).items
	return items
