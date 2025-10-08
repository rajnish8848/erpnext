# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
import frappe
from frappe.tests.utils import FrappeTestCase

class TestWBSMonthlyDistribution(FrappeTestCase):
	def setUp(self):
		from erpnext.accounts.doctype.payment_entry.test_payment_entry import create_company
		create_company()

	def tearDown(self):
		frappe.db.rollback()

	def test_wbs_monthly_distribution(self):
		project_name = "test_project" + frappe.generate_hash(length=5)
		if not frappe.db.exists("Project", {"project_name": project_name}):
			frappe.get_doc(
				{"doctype": "Project", "company": "_Test Company", "project_name": project_name, "is_wbs": 1}
			).insert()

		project = frappe.db.get_value("Project", {"project_name": project_name})

		wbs = frappe.get_doc(
			{
				"doctype": "Work Breakdown Structure",
				"project": project,
				"wbs_name": "test_wbs",
				"company": "_Test Company",
				"gl_account": "Cash - _TC",
			}
		)
		wbs.insert()
		wbs.submit()
		self.assertEqual(wbs.docstatus, 1)
		


		wbs_monthly_distribution = frappe.get_doc(
			{
				"doctype" : "WBS Monthly Distribution",
				"for_wbs" : wbs.name

			}
		)
		wbs_monthly_distribution.insert()
		wbs_monthly_distribution.submit()
		self.assertEqual(wbs_monthly_distribution.docstatus, 1)

		wbs_monthly_distribution1 = frappe.get_doc(
			{
				"doctype" : "WBS Monthly Distribution",
				"for_wbs" : wbs.name

			}
		)

		with self.assertRaises(frappe.exceptions.ValidationError) as context:
			wbs_monthly_distribution1.insert()

		self.assertIn(f"A record with the same WBS already exists: {wbs_monthly_distribution1.name}", str(context.exception))



	def test_wbs_monthly_distribution_update_linked_wbs(self):
		project_name = "test_project" + frappe.generate_hash(length=5)
		if not frappe.db.exists("Project", {"project_name": project_name}):
			frappe.get_doc(
				{"doctype": "Project", "company": "_Test Company", "project_name": project_name, "is_wbs": 1}
			).insert()

		project = frappe.db.get_value("Project", {"project_name": project_name})

		wbs = frappe.get_doc(
			{
				"doctype": "Work Breakdown Structure",
				"project": project,
				"wbs_name": "test_wbs",
				"company": "_Test Company",
				"gl_account": "Cash - _TC",
			}
		)
		wbs.insert()
		wbs.submit()
		self.assertEqual(wbs.docstatus, 1)
		


		wbs_monthly_distributuon = frappe.get_doc(
			{
				"doctype" : "WBS Monthly Distribution",
				"for_wbs" : wbs.name

			}
		)
		wbs_monthly_distributuon.insert()
		wbs.load_from_db()
		self.assertEqual(wbs.linked_monthly_distribution, wbs_monthly_distributuon.name)

		wbs_monthly_distributuon.delete()
		wbs.load_from_db()
		self.assertIsNone(wbs.linked_monthly_distribution)

