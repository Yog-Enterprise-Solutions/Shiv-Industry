// Copyright (c) 2024, YES and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gatekeeper View', {
	purchase_order: function (frm) {
		console.log("triggered")
		if (frm.doc.purchase_order != "") {			
			frappe.call({
				args: {
					purchase_order: frm.doc.purchase_order,
					name: frm.doc.name
				},
				method: "shiv_industry.shiv_industry.doctype.gatekeeper_view.gatekeeper_view.get_fields",
				callback: function (r) {
					var items = r['message']
					console.log(items);
					for (let item of items) {
						let row = frm.add_child("items");
						row.item_code = item.item_code;
						row.item_name = item.item_name;
						frm.refresh_fields('items');				
					}
				}
			});			
		}
		// frappe.msgprint(frm.doc.name)
	}
});
