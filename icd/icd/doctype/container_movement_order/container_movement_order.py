# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ContainerMovementOrder(Document):
	pass

import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder import Table

@frappe.whitelist()
def make_container_reception(source_name, target_doc=None):
    def set_missing_values(source, target):
        # You can set any default values if needed
        target.container_location = "Tanzania"  # example
        target.country_of_destination = "Tanzania"

    doc = get_mapped_doc(
        "Container Movement Order",
        source_name,
        {
            "Container Movement Order": {
                "doctype": "Container Reception",
                "field_map": {
                    "name": "movement_order",
                    "manifest": "manifest",
                    "company": "company",
                    "ship": "ship",
                    "port": "port",
                    "voyage_no": "voyage_no",
                    "ship_dc_date": "ship_dc_date",
                    "icd_time_in": "icd_time_in",
                    "port_time_out": "port_time_out",
                    "m_bl_no": "m_bl_no",
                    "container_no": "container_no",
                    "size_ft": "container_size_ft",
                    "cargo_type": "cargo_type",
                    "freight_indicator": "freight_indicator",
                    "tranporter": "transporter",
                    "truck": "truck",
                    "trailer": "trailer",
                    "driver": "driver",
                    "drive_license": "driver_license",
                },
            }
        },
        target_doc,
        set_missing_values,
    )

    return doc


@frappe.whitelist()
def get_containers_for_manifest(manifest: str, m_bl_no_filter: str | None = None):
    """Return list of containers from Manifest's child table `Containers`.

    Optionally filter by a partial `m_bl_no` string.
    """
    if not manifest:
        return []

    t = Table("tabContainers")
    query = (
        frappe.qb.from_(t)
        .select(
            t.name,
            t.container_no,
            t.m_bl_no,
            t.container_size,
            t.freight_indicator,
            t.type_of_container,
            t.no_of_packages,
            t.volume,
            t.volume_unit,
            t.weight,
            t.weight_unit,
            t.seal_no1,
            t.seal_no2,
            t.seal_no3,
            t.plug_type_of_reefer,
            t.minimum_temperature,
            t.maximum_temperature,
        )
        .where((t.parent == manifest) & (t.parenttype == "Manifest"))
    )

    if m_bl_no_filter:
        query = query.where(t.m_bl_no.like(f"%{m_bl_no_filter}%"))

    return query.run(as_dict=True)
