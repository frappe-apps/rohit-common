# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

def validate(self):
	self.validate_primary_address()
	self.validate_shipping_address()


def validate(doc,method):
	
	valid_chars_excise = "0123456789ABCDEFGIHJKLMNOPQRSTUVYWXZ"
	valid_chars_tin = "0123456789"
	
	if doc.excise_no != "NA":
		if len(doc.excise_no)!= 15:
			frappe.msgprint("Excise Number should be exactly as 15 digits or NA",raise_exception=1)
		else:
			for n, char in enumerate(reversed(doc.excise_no)):
				if not valid_chars_excise.count(char):
					frappe.msgprint("Only Numbers and alphabets in UPPERCASE are allowed in Excise Number or NA", raise_exception=1)

	if doc.service_tax_no != "NA":
		if len(doc.service_tax_no)!= 15:
			frappe.msgprint("Service Tax Number should be exactly as 15 digits or NA",raise_exception=1)
		else:
			for n, char in enumerate(reversed(doc.service_tax_no)):
				if not valid_chars_excise.count(char):
					frappe.msgprint("Only Numbers and alphabets in UPPERCASE are allowed in Service Tax Number or NA", raise_exception=1)

	if doc.tin_no != "NA":
		if len(doc.tin_no)!=11:
			frappe.msgprint("TIN Number should be exactly as 11 digits or NA",raise_exception=1)
		else:
			for n, char in enumerate(reversed(doc.tin_no)):
				if not valid_chars_tin.count(char):
					frappe.msgprint("Only Numbers are allowed in TIN Number or NA", raise_exception=1)
	
	def validate_primary_address(self):
		"""Validate that there can only be one primary address for particular customer, supplier"""
		if self.is_primary_address == 1:
			self._unset_other("is_primary_address")

		else:
			#This would check if there is any Primary Address if not then would make current as Primary address
			for fieldname in ["customer", "supplier", "sales_partner", "lead"]:
				if self.get(fieldname):
					if not frappe.db.sql("""select name from `tabAddress` where is_primary_address=1
						and `%s`=%s and name!=%s""" % (fieldname, "%s", "%s"),
						(self.get(fieldname), self.name)):
							self.is_primary_address = 1
					break

	def validate_shipping_address(self):
		"""Validate that there can only be one shipping address for particular customer, supplier"""
		if self.is_shipping_address == 1:
			self._unset_other("is_shipping_address")
		else:
			#This would check if there is any Shipping Address if not then would make current as Shipping address
			for fieldname in ["customer", "supplier", "sales_partner", "lead"]:
				if self.get(fieldname):
					if not frappe.db.sql("""select name from `tabAddress` where is_shipping_address=1
						and `%s`=%s and name!=%s""" % (fieldname, "%s", "%s"),
						(self.get(fieldname), self.name)):
							self.is_shipping_address = 1
					break

	def _unset_other(self, is_address_type):
		for fieldname in ["customer", "supplier", "sales_partner", "lead"]:
			if self.get(fieldname):
				frappe.db.sql("""update `tabAddress` set `%s`=0 where `%s`=%s and name!=%s""" %
					(is_address_type, fieldname, "%s", "%s"), (self.get(fieldname), self.name))
				break