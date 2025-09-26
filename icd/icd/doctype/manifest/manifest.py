# Copyright (c) 2025, Pal SHah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.xlsxutils import read_xlsx_file_from_attached_file
import os
import csv


def _normalize_header(value: str) -> str:
    """Return a normalized version of a header cell value for robust matching.

    Normalization rules:
    - lower-case
    - strip whitespace
    - remove punctuation-like characters commonly found in headers
    - collapse multiple spaces
    """
    if not value:
        return ""
    normalized = frappe.as_unicode(value).strip().lower()
    for token in ["/", "\\", ".", ",", "-", "(", ")", "[", "]", ":"]:
        normalized = normalized.replace(token, " ")
    normalized = " ".join(normalized.split())
    return normalized


def _build_header_index(header_row):
    """Build a map of normalized header -> column index."""
    index = {}
    for col_idx, raw in enumerate(header_row or []):
        key = _normalize_header(raw)
        if key and key not in index:
            index[key] = col_idx
    return index


def _get_cell(row, header_index, keys, default=None):
    """Fetch a cell by trying multiple header keys.

    - row: list of cell values
    - header_index: dict of normalized header -> index
    - keys: list of candidate header strings (un-normalized)
    """
    for key in keys:
        norm = _normalize_header(key)
        if norm in header_index:
            value = row[header_index[norm]] if header_index[norm] < len(row) else None
            return value if value is not None else default
    return default


class Manifest(Document):
    def validate(self):
        # If a manifest file is attached and has changed, parse it to populate containers
        try:
            # has_value_changed is available on Document in recent Frappe versions
            file_changed = getattr(self, "has_value_changed", lambda f: True)("upload_manifest")
        except Exception:
            file_changed = True

        if self.upload_manifest and file_changed:
            self._import_containers_from_attachment()

    def _import_containers_from_attachment(self):
        # Read rows from the attached file (xlsx or csv)
        rows = []
        file_url = self.upload_manifest
        ext = os.path.splitext(file_url or "")[1].lower()
        if ext == ".csv":
            # Read CSV via File doctype path
            _file = frappe.get_doc("File", {"file_url": file_url})
            filepath = _file.get_full_path()
            with open(filepath, mode="r", encoding="utf-8", newline="") as fh:
                reader = csv.reader(fh)
                rows = [list(col) for col in reader]
        else:
            rows = read_xlsx_file_from_attached_file(file_url=file_url)
        if not rows or len(rows) < 2:
            # nothing to import
            return

        # Find the first non-empty row to treat as headers
        header_row = None
        data_start_idx = 1
        for idx, row in enumerate(rows):
            if any(cell is not None and frappe.as_unicode(cell).strip() for cell in row):
                header_row = row
                data_start_idx = idx + 1
                break

        if not header_row:
            return

        header_index = _build_header_index(header_row)

        # Candidate headers mapping from Excel to child table fields
        header_candidates = {
            "m_bl_no": [
                "m b/l no",
                "master bl",
                "mbl no",
                "mbl",
            ],
            "container_no": [
                "container no",
                "container",
                "container number",
            ],
            "container_size": [
                "container size",
                "size",
                "container type",
            ],
            "no_of_packages": [
                "no of packages",
                "number of package",
                "packages",
            ],
        }

        # Vessel information candidates (pulled from FIRST data row only)
        vessel_candidates = {
            "mrn": ["mrn"],
            "vessel_name": ["vessel name", "vessel"],
            "call_sign": ["call sign", "callsign"],
            "voyage": ["voyage"],
            "tpa_uid": ["tpa uid", "tpa id"],
            "arrival_date": ["arrival date", "eta", "arrival"],
            "port": ["port", "port of discharge", "terminal"],
        }

        # Master BL child table candidates
        master_bl_candidates = {
            "m_bl_no": header_candidates["m_bl_no"],
            "bl_type": [
                "b/l type (master)",
                "bl type (master)",
                "bl type master",
                "master bl type",
            ],
            "port_of_loading": [
                "port of loading (master)",
                "loading port (master)",
                "pol (master)",
            ],
            "place_of_destination": [
                "port of destination (master)",
                "place of destination (master)",
                "destination (master)",
                "pod (master)",
            ],
            "number_of_containers": [
                "number of containers (master)",
                "no of containers (master)",
                "containers (master)",
            ],
        }

        # HBL Containers child table candidates
        hbl_cont_candidates = {
            "m_bl_no": header_candidates["m_bl_no"],
            "h_bl_no": [
                "house bl",
                "hbl no",
                "h bl no",
                "house b/l",
            ],
            "container_no": header_candidates["container_no"],
            "container_size": header_candidates["container_size"],
            "no_of_packages": header_candidates["no_of_packages"],
        }

        # House BL child table candidates (stored in field `table_axve`)
        house_bl_candidates = {
            "m_bl_no": header_candidates["m_bl_no"],
            "h_bl_no": [
                "house bl",
                "hbl no",
                "h bl no",
                "house b/l",
            ],
            "place_of_destination": [
                "port of destination (house)",
                "place of destination (house)",
                "destination (house)",
                "pod (house)",
            ],
            "number_of_containers": [
                "number of containers (house)",
                "no of containers (house)",
            ],
            "number_of_package": header_candidates["no_of_packages"],
        }

        # Clear existing child tables to avoid duplicates on re-import
        self.set("containers", [])
        self.set("hbl_conatiners", [])
        self.set("master_bl", [])
        self.set("table_axve", [])

        # If there is at least one data row, set vessel information from the first row
        if data_start_idx < len(rows):
            first_data_row = rows[data_start_idx]
            for fieldname, candidates in vessel_candidates.items():
                val = _get_cell(first_data_row, header_index, candidates)
                if val not in (None, ""):
                    try:
                        setattr(self, fieldname, val)
                    except Exception:
                        pass

        for row in rows[data_start_idx:]:
            # Skip empty rows
            if not any(cell is not None and frappe.as_unicode(cell).strip() for cell in row):
                continue

            child_values = {}

            for fieldname, candidates in header_candidates.items():
                val = _get_cell(row, header_index, candidates)
                if isinstance(val, str):
                    val = val.strip()
                child_values[fieldname] = val

            # Require at least container number or MBL to append a row
            if not child_values.get("container_no") and not child_values.get("m_bl_no"):
                continue

            # Normalize container size like 40FT/20FT etc.
            size_val = child_values.get("container_size")
            if isinstance(size_val, str):
                size_val = size_val.upper().replace(" FEET", "FT").replace("'", "")
                child_values["container_size"] = size_val

            self.append("containers", child_values)

            # HBL Containers row
            hbl_values = {}
            for fieldname, candidates in hbl_cont_candidates.items():
                val = _get_cell(row, header_index, candidates)
                if isinstance(val, str):
                    val = val.strip()
                hbl_values[fieldname] = val
            if hbl_values.get("h_bl_no") or hbl_values.get("container_no"):
                size_val = hbl_values.get("container_size")
                if isinstance(size_val, str):
                    size_val = size_val.upper().replace(" FEET", "FT").replace("'", "")
                    hbl_values["container_size"] = size_val
                self.append("hbl_conatiners", hbl_values)

            # Master BL row (dedupe based on key tuple)
            master_values = {}
            for fieldname, candidates in master_bl_candidates.items():
                val = _get_cell(row, header_index, candidates)
                if isinstance(val, str):
                    val = val.strip()
                master_values[fieldname] = val
            if not hasattr(self, "_seen_master_rows"):
                self._seen_master_rows = set()
            master_key = tuple(master_values.get(k) for k in [
                "m_bl_no", "bl_type", "port_of_loading", "place_of_destination", "number_of_containers"
            ])
            if any(v for v in master_key) and master_key not in self._seen_master_rows:
                self._seen_master_rows.add(master_key)
                self.append("master_bl", master_values)

            # House BL row (dedupe)
            house_values = {}
            for fieldname, candidates in house_bl_candidates.items():
                val = _get_cell(row, header_index, candidates)
                if isinstance(val, str):
                    val = val.strip()
                house_values[fieldname] = val
            if not hasattr(self, "_seen_house_rows"):
                self._seen_house_rows = set()
            house_key = tuple(house_values.get(k) for k in [
                "m_bl_no", "h_bl_no", "place_of_destination", "number_of_containers", "number_of_package"
            ])
            if any(v for v in house_key) and house_key not in self._seen_house_rows:
                self._seen_house_rows.add(house_key)
                self.append("table_axve", house_values)

        # Let the user know how many were imported in the UI
        if len(self.containers or []) > 0:
            frappe.msgprint(
                msg=frappe._("Imported {0} container rows from the attached manifest").format(len(self.containers)),
                alert=True,
            )
