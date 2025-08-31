# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Gatepass(Document):
	def on_submit(self):
		if self.container_id:
			doc = frappe.get_doc("Container Details",self.container_id)
			doc.db_set("status","Recevied")
