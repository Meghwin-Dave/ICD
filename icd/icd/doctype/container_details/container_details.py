# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate


class ContainerDetails(Document):
	def before_save(self):
		"""
		Auto-populate child rows in `date` table based on arrival date and totals.

		- Generate `total_days` rows starting from `arrival_date`
		- First `no_of_free_days` rows are marked as free (is_free = 1)
		- Remaining rows are billable (is_billable = 1)
		"""

		if not self.arrival_date or not self.total_days:
			return

		try:
			start_date = getdate(self.arrival_date)
		except Exception:
			# If date parsing fails, do nothing
			return

		total_days_int = int(self.total_days or 0)
		free_days_int = int(self.no_of_free_days or 0)

		# Rebuild the child table every save to reflect latest inputs
		self.set("date", [])

		for day_index in range(total_days_int):
			row = self.append("date", {})
			row.date = add_days(start_date, day_index)

			if day_index < free_days_int:
				row.is_free = 1
				row.is_billable = 0
			else:
				row.is_free = 0
				row.is_billable = 1
