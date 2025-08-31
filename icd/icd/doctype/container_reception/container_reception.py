# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ContainerReception(Document):
	def on_submit(self):
		# Create new Container Details doc
		container = frappe.new_doc("Container Details")

		# --- 1. Copy all fields directly from Container Reception ---
		reception_fields = [
			"container_no", "container_size_ft", "cargo_type", "freight_indicator",
			"m_bl_no", "country_of_destination", "transporter", "truck", "trailer",
			"driver", "driver_license", "icd_time_in", "port_time_out"
		]
		for field in reception_fields:
			if hasattr(self, field):
				setattr(container, field, getattr(self, field))

		# --- 2. Link back to Container Reception ---
		container.container_reception = self.name

		# --- 3. Fetch and copy from Movement Order (if linked) ---
		if self.movement_order:
			mo = frappe.get_doc("Container Movement Order", self.movement_order)
			mo_fields = [
				"manifest", "company", "ship", "port", "voyage_no",
				"ship_dc_date", "status", "tranporter", "driver",
				"drive_license", "truck", "trailer"
			]
			for field in mo_fields:
				if hasattr(mo, field):
					setattr(container, field, getattr(mo, field))

			container.movement_order = mo.name

		# --- 4. Fetch and copy from Manifest (if linked via MO or reception) ---
		manifest_name = None
		if self.manifest:
			manifest_name = self.manifest
		elif self.movement_order:
			mo = frappe.get_doc("Container Movement Order", self.movement_order)
			manifest_name = mo.manifest

		if manifest_name:
			manifest = frappe.get_doc("Manifest", manifest_name)
			manifest_fields = [
				"m_bl_no", "company", "ship", "port", "voyage_no",
				"ship_dc_date", "cargo_type", "freight_indicator", "size_ft"
			]
			for field in manifest_fields:
				if hasattr(manifest, field):
					setattr(container, field, getattr(manifest, field))

			container.manifest = manifest.name

		# --- 5. Default values for Container Details ---
		container.status = "In Yard"
		container.is_empty_container = 0

		# --- 6. Save ---
		container.insert(ignore_permissions=True)
		frappe.msgprint(f"✅ Container Details {container.name} created successfully.")

