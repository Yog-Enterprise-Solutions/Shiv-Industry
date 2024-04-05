import frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def polifo(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """
        SELECT name,supplier,status,transaction_date FROM `tabPurchase Order`
        ORDER BY creation desc;
        """
    )