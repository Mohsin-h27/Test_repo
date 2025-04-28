import unittest
import sys
import os

# Dynamically add the project root (two levels up) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import APIs.WorkdayStrategicSourcingAPISimulation as WorkdayStrategicSourcingAPI

###############################################################################
# Unit Tests
###############################################################################
class TestAttachmentsAPI(unittest.TestCase):
    """Tests for the API implementation."""

    def setUp(self):
        """Sets up the test environment."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB.clear()
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB.update({
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}})

    def test_attachments_get(self):
        """Tests the /attachments GET endpoint."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {
            "1": {"id": 1, "name": "file1"},
            "2": {"id": 2, "name": "file2"},
            "3": {"id": 3, "name": "file3"},
        }
        result = WorkdayStrategicSourcingAPI.Attachments.get("1,2")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[1]["id"], 2)

    def test_attachments_post(self):
        """Tests the /attachments POST endpoint."""
        data = {"name": "new_file"}
        result = WorkdayStrategicSourcingAPI.Attachments.post(data)
        self.assertEqual(result["name"], "new_file")
        self.assertIn(str(result["id"]), WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"])

    def test_attachment_by_id_get(self):
        """Tests the /attachments/{id} GET endpoint."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {"1": {"id": 1, "name": "file1"}}
        result = WorkdayStrategicSourcingAPI.Attachments.get_attachment_by_id(1)
        self.assertEqual(result, {"id": 1, "name": "file1"})
        self.assertIsNone(WorkdayStrategicSourcingAPI.Attachments.get_attachment_by_id(2))

    def test_attachment_by_id_patch(self):
        """Tests the /attachments/{id} PATCH endpoint."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {"1": {"id": 1, "name": "file1"}}
        data = {"name": "updated_file"}
        result = WorkdayStrategicSourcingAPI.Attachments.patch_attachment_by_id(1, data)
        self.assertEqual(result["name"], "updated_file")
        self.assertEqual(result["id"], 1)
        self.assertIsNone(WorkdayStrategicSourcingAPI.Attachments.patch_attachment_by_id(2, data))

    def test_attachment_by_id_delete(self):
        """Tests the /attachments/{id} DELETE endpoint."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {"1": {"id": 1, "name": "file1"}}
        result = WorkdayStrategicSourcingAPI.Attachments.delete_attachment_by_id(1)
        self.assertTrue(result)
        self.assertNotIn("1", WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"])
        self.assertFalse(WorkdayStrategicSourcingAPI.Attachments.delete_attachment_by_id(2))

    def test_attachment_by_external_id_get(self):
        """Tests the /attachments/{external_id}/external_id GET endpoint."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {"1": {"id": 1, "external_id": "ext1", "name": "file1"}}
        result = WorkdayStrategicSourcingAPI.Attachments.get_attachment_by_external_id("ext1")
        self.assertEqual(result, {"id": 1, "external_id": "ext1", "name": "file1"})
        self.assertIsNone(WorkdayStrategicSourcingAPI.Attachments.get_attachment_by_external_id("ext2"))

    def test_attachment_by_external_id_patch(self):
        """Tests the /attachments/{external_id}/external_id PATCH endpoint."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {"1": {"id": 1, "external_id": "ext1", "name": "file1"}}
        data = {"name": "updated_file"}
        result = WorkdayStrategicSourcingAPI.Attachments.patch_attachment_by_external_id("ext1", data)
        self.assertEqual(result["name"], "updated_file")
        self.assertEqual(result["external_id"], "ext1")
        self.assertIsNone(WorkdayStrategicSourcingAPI.Attachments.patch_attachment_by_external_id("ext2", data))

    def test_attachment_by_external_id_delete(self):
        """Tests the /attachments/{external_id}/external_id DELETE endpoint."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {"1": {"id": 1, "external_id": "ext1", "name": "file1"}}
        result = WorkdayStrategicSourcingAPI.Attachments.delete_attachment_by_external_id("ext1")
        self.assertTrue(result)
        self.assertNotIn("1", WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"])
        self.assertFalse(WorkdayStrategicSourcingAPI.Attachments.delete_attachment_by_external_id("ext2"))

    def test_state_persistence(self):
        """Tests state persistence."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {"1": {"id": 1, "name": "file1"}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_state.json")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_state.json")
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"], {"1": {"id": 1, "name": "file1"}})

    def test_list_attachments_empty(self):
        """Tests list_attachments with no attachments."""
        result = WorkdayStrategicSourcingAPI.Attachments.list_attachments()
        self.assertEqual(result["data"], [])
        self.assertEqual(result["meta"]["count"], 0)

    def test_list_attachments_with_data(self):
        """Tests list_attachments with existing attachments."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {
            "1": {"id": 1, "name": "file1"},
            "2": {"id": 2, "name": "file2"},
            "3": {"id": 3, "name": "file3"},
        }
        result = WorkdayStrategicSourcingAPI.Attachments.list_attachments()
        self.assertEqual(len(result["data"]), 3)
        self.assertEqual(result["meta"]["count"], 3)
        self.assertEqual(result["data"][0]["id"], 1)
        self.assertEqual(result["data"][1]["id"], 2)
        self.assertEqual(result["data"][2]["id"], 3)

    def test_list_attachments_filtered(self):
        """Tests list_attachments with a filter."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"] = {
            "1": {"id": 1, "name": "file1"},
            "2": {"id": 2, "name": "file2"},
            "3": {"id": 3, "name": "file3"},
        }
        filter_data =  "1,3"
        result = WorkdayStrategicSourcingAPI.Attachments.list_attachments(filter_id_equals=filter_data)
        self.assertEqual(len(result["data"]), 2)
        self.assertEqual(result["meta"]["count"], 2)
        self.assertEqual(result["data"][0]["id"], 1)
        self.assertEqual(result["data"][1]["id"], 3)

    def test_list_attachments_limit(self):
        """Tests list_attachments with a limit of 50."""
        for i in range(51):
            WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["attachments"][str(i)] = {"id": i, "name": f"file{i}"}
        result = WorkdayStrategicSourcingAPI.Attachments.list_attachments()
        self.assertEqual(len(result["data"]), 50)
        self.assertEqual(result["meta"]["count"], 50)

class TestAwardsAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
    'attachments': {},
    'awards': {"awards": [
                {"id": 1, "state": "active", "updated_at": "2023-01-01"},
                {"id": 2, "state": "inactive", "updated_at": "2023-02-01"},
                {"id": 3, "state": "active", "updated_at": "2023-03-01"},
            ],
            "award_line_items": [
                {"id": "ali1", "award_id": 1, "is_quoted": True, "line_item_type": "typeA"},
                {"id": "ali2", "award_id": 1, "is_quoted": False, "line_item_type": "typeB"},
                {"id": "ali3", "award_id": 2, "is_quoted": True, "line_item_type": "typeA"},
            ]},
    'contracts': {'award_line_items': [],
                'awards': {},
                'contract_types': {},
                'contracts': {}},
    'events': {'bid_line_items': {},
                'bids': {},
                'event_templates': {},
                'events': {},
                'line_items': {},
                'worksheets': {}},
    'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
    'payments': {'payment_currencies': [],
                'payment_currency_id_counter': "",
                'payment_term_id_counter': "",
                'payment_terms': [],
                'payment_type_id_counter': "",
                'payment_types': []},
    'projects': {'project_types': {}, 'projects': {}},
    'reports': {'contract_milestone_reports_entries': [],
                'contract_milestone_reports_schema': {},
                'contract_reports_entries': [],
                'contract_reports_schema': {},
                'event_reports': [],
                'event_reports_1_entries': [],
                'event_reports_entries': [],
                'event_reports_schema': {},
                'performance_review_answer_reports_entries': [],
                'performance_review_answer_reports_schema': {},
                'performance_review_reports_entries': [],
                'performance_review_reports_schema': {},
                'project_milestone_reports_entries': [],
                'project_milestone_reports_schema': {},
                'project_reports_1_entries': [],
                'project_reports_entries': [],
                'project_reports_schema': {},
                'savings_reports_entries': [],
                'savings_reports_schema': {},
                'supplier_reports_entries': [],
                'supplier_reports_schema': {},
                'supplier_review_reports_entries': [],
                'supplier_review_reports_schema': {},
                'suppliers': []},
    'scim': {'resource_types': [],
            'schemas': [],
            'service_provider_config': {},
            'users': []},
    'spend_categories': {},
    'suppliers': {'contact_types': {},
                'supplier_companies': {},
                'supplier_company_segmentations': {},
                'supplier_contacts': {}}}

        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_db.json")

    def tearDown(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_db.json")

    def test_awards_get(self):
        awards = WorkdayStrategicSourcingAPI.Awards.get(filter_state_equals=["active"])
        self.assertEqual(len(awards), 2)

        awards = WorkdayStrategicSourcingAPI.Awards.get(filter_updated_at_from="2023-02-01")
        self.assertEqual(len(awards), 2)

        awards = WorkdayStrategicSourcingAPI.Awards.get(filter_updated_at_to="2023-02-01")
        self.assertEqual(len(awards), 2)

    def test_award_line_items_get(self):
        line_items = WorkdayStrategicSourcingAPI.Awards.get_award_line_items(award_id=1)
        self.assertEqual(len(line_items), 2)

        line_items = WorkdayStrategicSourcingAPI.Awards.get_award_line_items(award_id=1, filter_is_quoted_equals=True)
        self.assertEqual(len(line_items), 1)

        line_items = WorkdayStrategicSourcingAPI.Awards.get_award_line_items(award_id=1, filter_line_item_type_equals=["typeA"])
        self.assertEqual(len(line_items), 1)

    def test_award_line_item_get(self):
        line_item = WorkdayStrategicSourcingAPI.Awards.get_award_line_item(id="ali1")
        self.assertIsNotNone(line_item)
        self.assertEqual(line_item["award_id"], 1)

        line_item = WorkdayStrategicSourcingAPI.Awards.get_award_line_item(id="nonexistent")
        self.assertIsNone(line_item)

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_persistence.json")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["awards"]["awards"].append({"id": 4, "state": "pending"})
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_persistence.json")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_persistence.json")
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["awards"]["awards"]), 4)

class TestContractsAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}
        self.test_contract = {"id": 1, "name": "Test Contract", "external_id": "ext1"}
        self.test_contract_type = {"id": 1, "name": "Test Type", "external_id": "ext_type_1"}

    def test_contracts_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get(), [self.test_contract])
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get(filter={"name": "Test Contract"}), [self.test_contract])
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get(filter={"name": "Nonexistent"}), [])

    def test_contracts_post(self):
        WorkdayStrategicSourcingAPI.Contracts.post(body=self.test_contract)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1], self.test_contract)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.post(body=None)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.post(body={"name": "test"})

    def test_contract_by_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get_contract_by_id(1), self.test_contract)
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.get_contract_by_id(2)

    def test_contract_by_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        updated_contract = {"id": 1, "name": "Updated Contract"}
        WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_id(1, body=updated_contract)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1]["name"], "Updated Contract")
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_id(2, body=updated_contract)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_id(1, body={"id":2, "name":"test"})
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_id(1, body=None)

    def test_contract_by_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        WorkdayStrategicSourcingAPI.Contracts.delete_contract_by_id(1)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"], {})
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.delete_contract_by_id(2)

    def test_contract_by_external_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get_contract_by_external_id("ext1"), self.test_contract)
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.get_contract_by_external_id("nonexistent")

    def test_contract_by_external_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        updated_contract = {"external_id": "ext1", "name": "Updated External Contract"}
        WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_external_id("ext1", body=updated_contract)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1]["name"], "Updated External Contract")
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_external_id("nonexistent", body=updated_contract)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_external_id("ext1", body={"external_id":"wrong","name":"test"})
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_by_external_id("ext1", body=None)

    def test_contract_by_external_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        WorkdayStrategicSourcingAPI.Contracts.delete_contract_by_external_id("ext1")
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"], {})
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.delete_contract_by_external_id("nonexistent")

    def test_contracts_describe_get(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get_contracts_description(), [])
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract
        self.assertEqual(sorted(WorkdayStrategicSourcingAPI.Contracts.get_contracts_description()), sorted(list(self.test_contract.keys())))

    def test_contract_types_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1] = self.test_contract_type
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get_contract_types(), [self.test_contract_type])

    def test_contract_types_post(self):
        WorkdayStrategicSourcingAPI.Contracts.post_contract_types(body=self.test_contract_type)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1], self.test_contract_type)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.post_contract_types(body=None)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.post_contract_types(body={"name":"test"})

    def test_contract_type_by_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1] = self.test_contract_type
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get_contract_type_by_id(1), self.test_contract_type)
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.get_contract_type_by_id(2)

    def test_contract_type_by_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1] = self.test_contract_type
        updated_contract_type = {"id": 1, "name": "Updated Type"}
        WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_id(1, body=updated_contract_type)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1]["name"], "Updated Type")
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_id(2, body=updated_contract_type)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_id(1, body={"id":2,"name":"test"})
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_id(1, body=None)

    def test_contract_type_by_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1] = self.test_contract_type
        WorkdayStrategicSourcingAPI.Contracts.delete_contract_type_by_id(1)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"], {})
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.delete_contract_type_by_id(2)

    def test_contract_type_by_external_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1] = self.test_contract_type
        self.assertEqual(WorkdayStrategicSourcingAPI.Contracts.get_contract_type_by_external_id("ext_type_1"), self.test_contract_type)
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.get_contract_type_by_external_id("nonexistent")

    def test_contract_type_by_external_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1] = self.test_contract_type
        updated_contract_type = {"external_id": "ext_type_1", "name": "Updated External Type"}
        WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_external_id("ext_type_1", body=updated_contract_type)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1]["name"], "Updated External Type")
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_external_id("nonexistent", body=updated_contract_type)
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_external_id("ext_type_1", body={"external_id":"wrong","name":"test"})
        with self.assertRaises(ValueError):
            WorkdayStrategicSourcingAPI.Contracts.patch_contract_type_by_external_id("ext_type_1", body=None)

    def test_contract_type_by_external_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"][1] = self.test_contract_type
        WorkdayStrategicSourcingAPI.Contracts.delete_contract_type_by_external_id("ext_type_1")
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contract_types"], {})
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.Contracts.delete_contract_type_by_external_id("nonexistent")

    def test_state_persistence(self):
        if "contracts" not in WorkdayStrategicSourcingAPI.SimulationEngine.db.DB:
            WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"] = {}  # Ensure it's a dictionary

        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"][1] = self.test_contract  # Store the contract safely
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_state.json")  # Save state

        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"] = {}  # Clear contracts to simulate fresh load
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_state.json")  # Reload from saved state

        value = WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["contracts"]["contracts"].get('1')
        self.assertEqual(value, self.test_contract)  # Validate contract exists



class TestContractAward(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {"contracts": {},
                          "contract_types": {},
                          "awards": {1: {"id":1, "name":"Award 1"}},
                          "award_line_items": []},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}

    def test_contract_list_awards(self):
        response = WorkdayStrategicSourcingAPI.ContractAward.list_awards()
        self.assertEqual(response, [{"id":1, "name":"Award 1"}])

    def test_contract_get_award(self):
        response = WorkdayStrategicSourcingAPI.ContractAward.get_award(1)
        self.assertEqual(response, {"id":1, "name":"Award 1"})
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.ContractAward.get_award(2)

class TestContractAwardLineItem(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {"contracts": {},
                          "contract_types": {},
                          "awards": {1: {"id":1, "name":"Award 1"}},
                          "award_line_items": [{"id":"ali1", "award_id": 1}, {"id":"ali2", "award_id": 2}]
                          },
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}

    def test_contract_list_award_line_items(self):
        response = WorkdayStrategicSourcingAPI.ContractAward.list_contract_award_line_items(1)
        self.assertEqual(response, [{"id":"ali1", "award_id": 1}])
        response = WorkdayStrategicSourcingAPI.ContractAward.list_contract_award_line_items(2)
        self.assertEqual(response, [{"id":"ali2", "award_id": 2}])
        self.assertEqual(WorkdayStrategicSourcingAPI.ContractAward.list_contract_award_line_items(3), [])

    def test_contract_get_award_line_item(self):
        response = WorkdayStrategicSourcingAPI.ContractAward.get_contract_award_line_item("ali1")
        self.assertEqual(response, {"id":"ali1", "award_id": 1})
        with self.assertRaises(KeyError):
            WorkdayStrategicSourcingAPI.ContractAward.get_contract_award_line_item("nonexistent")

class TestEventsAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {
                        "event_templates": {1: {"name": "Template 1"}},
                        "events": {
                            1: {"name": "Event 1", "type": "RFP", "external_id": "event_ext_1"},
                            2: {"name": "Event 2", "type": "Other"},
                            3: {"name": "Event 3", "external_id": "event_ext_2"}
                        },
                        "worksheets": {1: {"event_id": 1, "name": "Worksheet 1"}},
                        "line_items": {1: {"event_id": 1, "worksheet_id": 1, "name": "Line Item 1"}},
                        "bids": {1: {"event_id": 1, "supplier_id": 1, "status": "submitted"}},
                        "bid_line_items": {1: {"bid_id": 1, "item_name": "Bid Line Item 1", "price": 100}}
                      },
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}

        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_db.json")

    def tearDown(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_db.json")

    def test_event_templates_get(self):
        templates = WorkdayStrategicSourcingAPI.EventTemplates.get()
        self.assertEqual(len(templates), 1)

    def test_event_templates_get_by_id(self):
        template = WorkdayStrategicSourcingAPI.EventTemplates.get_by_id(1)
        self.assertIsNotNone(template)
        template = WorkdayStrategicSourcingAPI.EventTemplates.get_by_id(2)
        self.assertIsNone(template)

    def test_events_get(self):
        events = WorkdayStrategicSourcingAPI.Events.get()
        self.assertEqual(len(events), 3)
        events = WorkdayStrategicSourcingAPI.Events.get(filter={"type": "RFP"})
        self.assertEqual(len(events), 1)

    def test_events_post(self):
        new_event = WorkdayStrategicSourcingAPI.Events.post({"name": "New Event", "project_id": 1})
        self.assertIsNotNone(new_event)
        self.assertIn(new_event["id"], WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["events"]["events"])

    def test_events_get_by_id(self):
        event = WorkdayStrategicSourcingAPI.Events.get_by_id(1)
        self.assertIsNotNone(event)
        event = WorkdayStrategicSourcingAPI.Events.get_by_id(4)
        self.assertIsNone(event)

    def test_events_patch(self):
        updated_event = WorkdayStrategicSourcingAPI.Events.patch(1, {"name": "Updated Event", "id":1})
        self.assertIsNotNone(updated_event)
        self.assertEqual(updated_event["name"], "Updated Event")
        updated_event = WorkdayStrategicSourcingAPI.Events.patch(4, {"name": "Updated Event"})
        self.assertIsNone(updated_event)
        updated_event = WorkdayStrategicSourcingAPI.Events.patch(1, {"name": "Updated Event", "id":2})
        self.assertIsNone(updated_event)

    def test_events_delete(self):
        result = WorkdayStrategicSourcingAPI.Events.delete(1)
        self.assertTrue(result)
        result = WorkdayStrategicSourcingAPI.Events.delete(4)
        self.assertFalse(result)

    def test_event_worksheets_get(self):
        worksheets = WorkdayStrategicSourcingAPI.EventWorksheets.get(1)
        self.assertEqual(len(worksheets), 1)

    def test_event_worksheet_by_id_get(self):
        worksheet = WorkdayStrategicSourcingAPI.EventWorksheetById.get(1, 1)
        self.assertIsNotNone(worksheet)
        worksheet = WorkdayStrategicSourcingAPI.EventWorksheetById.get(1, 2)
        self.assertIsNone(worksheet)

    def test_event_worksheet_line_items_get(self):
        line_items = WorkdayStrategicSourcingAPI.EventWorksheetLineItems.get(1, 1)
        self.assertEqual(len(line_items), 1)

    def test_event_worksheet_line_items_post(self):
        new_line_item = WorkdayStrategicSourcingAPI.EventWorksheetLineItems.post(1, 1, {"name": "New Line Item"})
        self.assertIsNotNone(new_line_item)
        self.assertIn(new_line_item["id"], WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["events"]["line_items"])

    def test_event_worksheet_line_items_post_multiple(self):
        new_line_items = WorkdayStrategicSourcingAPI.EventWorksheetLineItems.post_multiple(1, 1, [{"name": "New Line Item 1"}, {"name": "New Line Item 2"}])
        self.assertEqual(len(new_line_items), 2)
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["events"]["line_items"]), 3)

    def test_event_worksheet_line_item_by_id_get(self):
        line_item = WorkdayStrategicSourcingAPI.EventWorksheetLineItemById.get(1, 1, 1)
        self.assertIsNotNone(line_item)
        line_item = WorkdayStrategicSourcingAPI.EventWorksheetLineItemById.get(1, 1, 2)
        self.assertIsNone(line_item)

    def test_event_worksheet_line_item_by_id_patch(self):
        updated_line_item = WorkdayStrategicSourcingAPI.EventWorksheetLineItemById.patch(1, 1, 1, {"name": "Updated Line Item", "id":1})
        self.assertIsNotNone(updated_line_item)
        self.assertEqual(updated_line_item["name"], "Updated Line Item")

    def test_event_worksheet_line_item_by_id_delete(self):
        result = WorkdayStrategicSourcingAPI.EventWorksheetLineItemById.delete(1, 1, 1)
        self.assertTrue(result)

    def test_event_supplier_companies_post(self):
        result = WorkdayStrategicSourcingAPI.EventSupplierCompanies.post(1, {"supplier_ids": [1, 2]})
        self.assertIsNotNone(result)
        self.assertIn(1, result["suppliers"])
        self.assertIn(2, result["suppliers"])
        self.assertIsNone(WorkdayStrategicSourcingAPI.EventSupplierCompanies.post(2, {"supplier_ids": [1,2]}))

    def test_event_supplier_companies_delete(self):
        WorkdayStrategicSourcingAPI.EventSupplierCompanies.post(1, {"supplier_ids": [1, 2]})
        result = WorkdayStrategicSourcingAPI.EventSupplierCompanies.delete(1, {"supplier_ids": [1]})
        self.assertIsNotNone(result)
        self.assertNotIn(1, result["suppliers"])

    def test_event_supplier_companies_external_id_post(self):
        result = WorkdayStrategicSourcingAPI.EventSupplierCompaniesExternalId.post("event_ext_1", {"supplier_external_ids": ["ext_1", "ext_2"]})
        self.assertIsNotNone(result)
        self.assertIn("ext_1", result["suppliers"])
        self.assertIsNone(WorkdayStrategicSourcingAPI.EventSupplierCompaniesExternalId.post("event_ext_invalid", {"supplier_external_ids": ["ext_1"]}))

    def test_event_supplier_companies_external_id_delete(self):
        WorkdayStrategicSourcingAPI.EventSupplierCompaniesExternalId.post("event_ext_1", {"supplier_external_ids": ["ext_1", "ext_2"]})
        result = WorkdayStrategicSourcingAPI.EventSupplierCompaniesExternalId.delete("event_ext_1", {"supplier_external_ids": ["ext_1"]})
        self.assertIsNotNone(result)
        self.assertNotIn("ext_1", result["suppliers"])
        self.assertIsNone(WorkdayStrategicSourcingAPI.EventSupplierCompaniesExternalId.delete("event_ext_invalid", {"supplier_external_ids": ["ext_1"]}))

    def test_event_supplier_contacts_post(self):
        result = WorkdayStrategicSourcingAPI.EventSupplierContacts.post(1, {"supplier_contact_ids": [1, 2]})
        self.assertIsNotNone(result)
        self.assertIn(1, result["supplier_contacts"])
        self.assertIn(2, result["supplier_contacts"])

    def test_event_supplier_contacts_delete(self):
        WorkdayStrategicSourcingAPI.EventSupplierContacts.post(1, {"supplier_contact_ids": [1, 2]})
        result = WorkdayStrategicSourcingAPI.EventSupplierContacts.delete(1, {"supplier_contact_ids": [1]})
        self.assertIsNotNone(result)
        self.assertNotIn(1, result["supplier_contacts"])

    def test_event_supplier_contacts_external_id_post(self):
        result = WorkdayStrategicSourcingAPI.EventSupplierContactsExternalId.post("event_ext_1", {"supplier_contact_external_ids": ["contact_ext_1", "contact_ext_2"]})
        self.assertIsNotNone(result)
        self.assertIn("contact_ext_1", result["supplier_contacts"])

    def test_event_supplier_contacts_external_id_delete(self):
        WorkdayStrategicSourcingAPI.EventSupplierContactsExternalId.post("event_ext_1", {"supplier_contact_external_ids": ["contact_ext_1", "contact_ext_2"]})
        result = WorkdayStrategicSourcingAPI.EventSupplierContactsExternalId.delete("event_ext_1", {"supplier_contact_external_ids": ["contact_ext_1"]})
        self.assertIsNotNone(result)
        self.assertNotIn("contact_ext_1", result["supplier_contacts"])

    def test_event_bids_get(self):
        bids = WorkdayStrategicSourcingAPI.EventBids.get(1)
        self.assertEqual(len(bids), 1)
        bids = WorkdayStrategicSourcingAPI.EventBids.get(2)
        self.assertEqual(len(bids), 0)
        bids = WorkdayStrategicSourcingAPI.EventBids.get(1, filter={"status": "submitted"})
        self.assertEqual(len(bids), 1)
        bids = WorkdayStrategicSourcingAPI.EventBids.get(1, page={"size": 1})
        self.assertEqual(len(bids), 1)

    def test_bids_by_id_get(self):
        bid = WorkdayStrategicSourcingAPI.BidsById.get(1)
        self.assertIsNotNone(bid)
        bid = WorkdayStrategicSourcingAPI.BidsById.get(2)
        self.assertIsNone(bid)

    def test_bids_describe(self):
        fields = WorkdayStrategicSourcingAPI.BidsDescribe.get()
        self.assertIn("event_id", fields)

    def test_bid_line_items_get(self):
        line_items = WorkdayStrategicSourcingAPI.BidLineItems.get(1)
        self.assertEqual(len(line_items), 1)

    def test_bid_line_item_by_id_get(self):
        line_item = WorkdayStrategicSourcingAPI.BidLineItemById.get(1)
        self.assertIsNotNone(line_item)
        line_item = WorkdayStrategicSourcingAPI.BidLineItemById.get(2)
        self.assertIsNone(line_item)

    def test_bid_line_items_list_get(self):
        line_items = WorkdayStrategicSourcingAPI.BidLineItemsList.get()
        self.assertEqual(len(line_items), 1)
        line_items = WorkdayStrategicSourcingAPI.BidLineItemsList.get(filter={"price": 100})
        self.assertEqual(len(line_items), 1)

    def test_bid_line_items_describe(self):
        fields = WorkdayStrategicSourcingAPI.BidLineItemsDescribe.get()
        self.assertIn("bid_id", fields)

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_persistence.json")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["events"]["events"][1]["name"] = "Modified Event"
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_persistence.json")
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["events"]["events"]['1']["name"], "Event 1")

class TestFieldsAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {
                        "fields": {1: {"id": 1, "name": "field1"}, 2: {"id": 2, "name": "field2"}},
                        "field_options": {1: {"id": 1, "field_id": 1}, 2: {"id": 2, "field_id": 2}},
                        "field_groups": {1: {"id": 1, "name": "group1"}, 2: {"id": 2, "name": "group2"}}
                      },
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}


        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_state.json")

    def tearDown(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_state.json")

    def test_fields_get(self):
        fields = WorkdayStrategicSourcingAPI.Fields.get()
        self.assertEqual(1, fields[0]["id"])
        self.assertEqual(len(fields), 2)
        filtered_fields = WorkdayStrategicSourcingAPI.Fields.get(filter={"name": "field1"})
        self.assertEqual(len(filtered_fields), 1)

    def test_fields_post(self):
        new_field = WorkdayStrategicSourcingAPI.Fields.post(3, {'id':3})
        self.assertEqual(new_field["id"], 3)
        self.assertIn(3, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["fields"])

    def test_field_by_id_get(self):
        field = WorkdayStrategicSourcingAPI.FieldById.get('1')
        self.assertEqual(field["id"], 1)
        self.assertIsNone(WorkdayStrategicSourcingAPI.FieldById.get(99))

    def test_field_by_id_patch(self):
        field = WorkdayStrategicSourcingAPI.FieldById.patch(1, {'id':1})
        self.assertEqual(field["id"], 1)
        self.assertIsNone(WorkdayStrategicSourcingAPI.FieldById.patch(99, {}))

    def test_field_by_id_delete(self):
        result = WorkdayStrategicSourcingAPI.FieldById.delete('1')
        self.assertTrue(result)
        self.assertNotIn(1, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["fields"])
        self.assertFalse(WorkdayStrategicSourcingAPI.FieldById.delete(99))

    def test_field_options_by_field_id_get(self):
        options = WorkdayStrategicSourcingAPI.FieldOptionsByFieldId.get(1)
        self.assertEqual(len(options), 1)
        self.assertEqual(options[0]["id"], 1)

    def test_field_options_post(self):
        result = WorkdayStrategicSourcingAPI.FieldOptions.post("F001", ["New", "Ongoing", "Closed"])
        self.assertEqual(result, {"field_id": "F001", "options": ["New", "Ongoing", "Closed"]})
        self.assertIn("F001", WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["field_options"])

    def test_field_option_by_id_patch(self):
        """Test updating an existing field option."""
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["field_options"]["F001"] = {"field_id": "F001", "options": ["New", "Ongoing", "Closed"]}
        result = WorkdayStrategicSourcingAPI.FieldOptionById.patch("F001", ["Updated", "Values"])
        self.assertEqual(result, {"field_id": "F001", "options": ["Updated", "Values"]})
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["field_options"]["F001"]["options"], ["Updated", "Values"])

    def test_field_option_by_id_delete(self):
        result = WorkdayStrategicSourcingAPI.FieldOptionById.delete(1)
        self.assertTrue(result)
        self.assertNotIn(1, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["field_options"])
        self.assertFalse(WorkdayStrategicSourcingAPI.FieldOptionById.delete(99))

    def test_field_groups_get(self):
        groups = WorkdayStrategicSourcingAPI.FieldGroups.get()
        self.assertEqual(len(groups), 2)

    def test_field_groups_post(self):
        result = WorkdayStrategicSourcingAPI.FieldGroups.post("New Group", "Group Description")
        self.assertIn("id", result)
        self.assertEqual(result["name"], "New Group")
        self.assertEqual(result["description"], "Group Description")
        self.assertIn(result["id"], WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["field_groups"])

    def test_field_group_by_id_get(self):
        group = WorkdayStrategicSourcingAPI.FieldGroupById.get(1)
        self.assertEqual(group["id"], 1)
        self.assertIsNone(WorkdayStrategicSourcingAPI.FieldGroupById.get(99))

    def test_field_group_by_id_patch(self):
        group = WorkdayStrategicSourcingAPI.FieldGroupById.patch(1, {'id': 1})
        self.assertEqual(group["id"], 1)
        self.assertIsNone(WorkdayStrategicSourcingAPI.FieldGroupById.patch(99, {}))

    def test_field_group_by_id_delete(self):
        result = WorkdayStrategicSourcingAPI.FieldGroupById.delete(1)
        self.assertTrue(result)
        self.assertNotIn(1, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["field_groups"])
        self.assertFalse(WorkdayStrategicSourcingAPI.FieldGroupById.delete(99))

    def test_state_loading_nonexistent_file(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["fields"] = {1: {"id": 1}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("nonexistent_file.json")
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["fields"]["fields"]), 1)

class TestPaymentAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {
                        "payment_terms": [],
                        "payment_types": [],
                        "payment_currencies": [],
                        "payment_term_id_counter": 1,
                        "payment_type_id_counter": 1,
                        "payment_currency_id_counter": 1,
                        },
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}

        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_state.json")

    def tearDown(self):
        if os.path.exists("test_state.json"):
            os.remove("test_state.json")

    def test_payment_terms_get_post(self):
        terms = WorkdayStrategicSourcingAPI.PaymentTerms.get()
        self.assertEqual(len(terms), 0)

        term1 = WorkdayStrategicSourcingAPI.PaymentTerms.post(name="Net 30", external_id="NET30")
        self.assertEqual(term1["name"], "Net 30")
        self.assertEqual(term1["external_id"], "NET30")
        self.assertEqual(term1["id"], 1)

        terms = WorkdayStrategicSourcingAPI.PaymentTerms.get()
        self.assertEqual(len(terms), 1)

    def test_payment_terms_id_patch_delete(self):
        term1 = WorkdayStrategicSourcingAPI.PaymentTerms.post(name="Net 30", external_id="NET30")
        updated_term = WorkdayStrategicSourcingAPI.PaymentTermsId.patch(id=term1["id"], name="Net 60")
        self.assertEqual(updated_term["name"], "Net 60")

        deleted = WorkdayStrategicSourcingAPI.PaymentTermsId.delete(id=term1["id"])
        self.assertTrue(deleted)

        terms = WorkdayStrategicSourcingAPI.PaymentTerms.get()
        self.assertEqual(len(terms), 0)

    def test_payment_terms_external_id_patch_delete(self):
        term1 = WorkdayStrategicSourcingAPI.PaymentTerms.post(name="Net 30", external_id="NET30")
        updated_term = WorkdayStrategicSourcingAPI.PaymentTermsExternalId.patch(external_id="NET30", name="Net 90")
        self.assertEqual(updated_term["name"], "Net 90")

        deleted = WorkdayStrategicSourcingAPI.PaymentTermsExternalId.delete(external_id="NET30")
        self.assertTrue(deleted)

        terms = WorkdayStrategicSourcingAPI.PaymentTerms.get()
        self.assertEqual(len(terms), 0)

    def test_payment_types_get_post(self):
        types = WorkdayStrategicSourcingAPI.PaymentTypes.get()
        self.assertEqual(len(types), 0)

        type1 = WorkdayStrategicSourcingAPI.PaymentTypes.post(name="Credit Card", payment_method="Visa", external_id="CC")
        self.assertEqual(type1["name"], "Credit Card")
        self.assertEqual(type1["payment_method"], "Visa")
        self.assertEqual(type1["external_id"], "CC")
        self.assertEqual(type1["id"], 1)

        types = WorkdayStrategicSourcingAPI.PaymentTypes.get()
        self.assertEqual(len(types), 1)

    def test_payment_types_id_patch_delete(self):
        type1 = WorkdayStrategicSourcingAPI.PaymentTypes.post(name="Credit Card", payment_method="Visa", external_id="CC")
        updated_type = WorkdayStrategicSourcingAPI.PaymentTypesId.patch(id=type1["id"], name="Debit Card", payment_method="Mastercard")
        self.assertEqual(updated_type["name"], "Debit Card")
        self.assertEqual(updated_type["payment_method"], "Mastercard")

        deleted = WorkdayStrategicSourcingAPI.PaymentTypesId.delete(id=type1["id"])
        self.assertTrue(deleted)

        types = WorkdayStrategicSourcingAPI.PaymentTypes.get()
        self.assertEqual(len(types), 0)

    def test_payment_types_external_id_patch_delete(self):
        type1 = WorkdayStrategicSourcingAPI.PaymentTypes.post(name="Credit Card", payment_method="Visa", external_id="CC")
        updated_type = WorkdayStrategicSourcingAPI.PaymentTypesExternalId.patch(external_id="CC", name="Amex", payment_method="American Express")
        self.assertEqual(updated_type["name"], "Amex")
        self.assertEqual(updated_type["payment_method"], "American Express")

        deleted = WorkdayStrategicSourcingAPI.PaymentTypesExternalId.delete(external_id="CC")
        self.assertTrue(deleted)

        types = WorkdayStrategicSourcingAPI.PaymentTypes.get()
        self.assertEqual(len(types), 0)

    def test_payment_currencies_get_post(self):
        currencies = WorkdayStrategicSourcingAPI.PaymentCurrencies.get()
        self.assertEqual(len(currencies), 0)

        currency1 = WorkdayStrategicSourcingAPI.PaymentCurrencies.post(alpha="USD", numeric="840", external_id="US")
        self.assertEqual(currency1["alpha"], "USD")
        self.assertEqual(currency1["numeric"], "840")
        self.assertEqual(currency1["external_id"], "US")
        self.assertEqual(currency1["id"], 1)

        currencies = WorkdayStrategicSourcingAPI.PaymentCurrencies.get()
        self.assertEqual(len(currencies), 1)

    def test_payment_currencies_id_patch_delete(self):
        currency1 = WorkdayStrategicSourcingAPI.PaymentCurrencies.post(alpha="USD", numeric="840", external_id="US")
        updated_currency = WorkdayStrategicSourcingAPI.PaymentCurrenciesId.patch(id=currency1["id"], alpha="EUR", numeric="978")
        self.assertEqual(updated_currency["alpha"], "EUR")
        self.assertEqual(updated_currency["numeric"], "978")

        deleted = WorkdayStrategicSourcingAPI.PaymentCurrenciesId.delete(id=currency1["id"])
        self.assertTrue(deleted)

        currencies = WorkdayStrategicSourcingAPI.PaymentCurrencies.get()
        self.assertEqual(len(currencies), 0)

    def test_payment_currencies_external_id_patch_delete(self):
        currency1 = WorkdayStrategicSourcingAPI.PaymentCurrencies.post(alpha="USD", numeric="840", external_id="US")
        updated_currency = WorkdayStrategicSourcingAPI.PaymentCurrenciesExternalId.patch(external_id="US", alpha="GBP", numeric="826")
        self.assertEqual(updated_currency["alpha"], "GBP")
        self.assertEqual(updated_currency["numeric"], "826")

        deleted = WorkdayStrategicSourcingAPI.PaymentCurrenciesExternalId.delete(external_id="US")
        self.assertTrue(deleted)

        currencies = WorkdayStrategicSourcingAPI.PaymentCurrencies.get()
        self.assertEqual(len(currencies), 0)

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.PaymentTerms.post(name="Net 30", external_id="NET30")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_state.json")

        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {
                        "payment_terms": [],
                        "payment_types": [],
                        "payment_currencies": [],
                        "payment_term_id_counter": 1,
                        "payment_type_id_counter": 1,
                        "payment_currency_id_counter": 1,
                        },
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}

        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_state.json")
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["payments"]["payment_terms"]), 1)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["payments"]["payment_terms"][0]["name"], "Net 30")

class TestProjectsAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}

        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"] = {
            1: {"id": 1, "name": "Project 1", "external_id": "ext1"},
            2: {"id": 2, "name": "Project 2", "external_id": "ext2"},
        }
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["project_types"] = {1: {"id": 1, "name": "Type 1"}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_db.json")

    def tearDown(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_db.json")

    def test_projects_get(self):
        projects = WorkdayStrategicSourcingAPI.Projects.get()
        self.assertEqual(len(projects), 2)

    def test_projects_get_filter(self):
        projects = WorkdayStrategicSourcingAPI.Projects.get(filter={"name": "Project 1"})
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["name"], "Project 1")

    def test_projects_get_page(self):
        projects = WorkdayStrategicSourcingAPI.Projects.get(page={"size": 1})
        self.assertEqual(len(projects), 1)

    def test_projects_post(self):
        new_project = {"name": "New Project", "external_id": "ext3"}
        created_project = WorkdayStrategicSourcingAPI.Projects.post(new_project)
        self.assertEqual(created_project["name"], "New Project")
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"]), 3)

    def test_project_by_id_get(self):
        project = WorkdayStrategicSourcingAPI.ProjectById.get(1)
        self.assertEqual(project["name"], "Project 1")

    def test_project_by_id_patch(self):
        updated_project = WorkdayStrategicSourcingAPI.ProjectById.patch(1, {"id": 1, "name": "Updated Project"})
        self.assertEqual(updated_project["name"], "Updated Project")

    def test_project_by_id_delete(self):
        result = WorkdayStrategicSourcingAPI.ProjectById.delete(1)
        self.assertTrue(result)
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"]), 1)

    def test_project_by_external_id_get(self):
        project = WorkdayStrategicSourcingAPI.ProjectByExternalId.get("ext1")
        self.assertEqual(project["name"], "Project 1")

    def test_project_by_external_id_patch(self):
        updated_project = WorkdayStrategicSourcingAPI.ProjectByExternalId.patch("ext1", {"external_id": "ext1", "name": "Updated Ext Project"})
        self.assertEqual(updated_project["name"], "Updated Ext Project")

    def test_project_by_external_id_delete(self):
        result = WorkdayStrategicSourcingAPI.ProjectByExternalId.delete("ext1")
        self.assertTrue(result)
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"]), 1)

    def test_projects_describe_get(self):
        fields = WorkdayStrategicSourcingAPI.ProjectsDescribe.get()
        self.assertIn("name", fields)

    def test_project_relationships_supplier_companies_post(self):
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierCompanies.post(1, [10, 20])
        self.assertTrue(result)
        self.assertIn(10, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_companies"])

    def test_project_relationships_supplier_companies_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_companies"] = [10, 20]
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierCompanies.delete(1, [10])
        self.assertTrue(result)
        self.assertNotIn(10, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_companies"])

    def test_project_relationships_supplier_companies_external_id_post(self):
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierCompaniesExternalId.post("ext1", ["10", "20"])
        self.assertTrue(result)
        self.assertIn("10", WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_companies"])

    def test_project_relationships_supplier_companies_external_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_companies"] = ["10", "20"]
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierCompaniesExternalId.delete("ext1", ["10"])
        self.assertTrue(result)
        self.assertNotIn("10", WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_companies"])

    def test_project_relationships_supplier_contacts_post(self):
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierContacts.post(1, [30, 40])
        self.assertTrue(result)
        self.assertIn(30, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_contacts"])

    def test_project_relationships_supplier_contacts_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_contacts"] = [30, 40]
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierContacts.delete(1, [30])
        self.assertTrue(result)
        self.assertNotIn(30, WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_contacts"])

    def test_project_relationships_supplier_contacts_external_id_post(self):
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierContactsExternalId.post("ext1", ["30", "40"])
        self.assertTrue(result)
        self.assertIn("30", WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_contacts"])

    def test_project_relationships_supplier_contacts_external_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_contacts"] = ["30", "40"]
        result = WorkdayStrategicSourcingAPI.ProjectRelationshipsSupplierContactsExternalId.delete("ext1", ["30"])
        self.assertTrue(result)
        self.assertNotIn("30", WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["supplier_contacts"])

    def test_project_types_get(self):
        project_types = WorkdayStrategicSourcingAPI.ProjectTypes.get()
        self.assertEqual(len(project_types), 1)

    def test_project_type_by_id_get(self):
        project_type = WorkdayStrategicSourcingAPI.ProjectTypeById.get(1)
        self.assertEqual(project_type["name"], "Type 1")

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_persistence.json")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"][1]["name"] = "Modified Project"
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_persistence.json")
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]["projects"]['1']["name"], "Project 1")

    def test_state_load_nonexistent_file(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("nonexistent.json")
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"], {"projects": {1: {'id': 1, 'name': 'Project 1', 'external_id': 'ext1'}, 2: {'id': 2, 'name': 'Project 2', 'external_id': 'ext2'}}, 'project_types': {1: {'id': 1, 'name': 'Type 1'}}})

class TestReportsAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {'payment_currencies': [],
                        'payment_currency_id_counter': "",
                        'payment_term_id_counter': "",
                        'payment_terms': [],
                        'payment_type_id_counter': "",
                        'payment_types': []},
            'projects': {'project_types': {}, 'projects': {}},
            'reports':  {
                        'contract_milestone_reports_entries': [{'id': 1, 'name': 'Milestone 1'}],
                        'contract_milestone_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'contract_reports_entries': [{'id': 1, 'contract_name': 'Contract 1'}],
                        'contract_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'event_reports_entries': [{'id': 1, 'event_name': 'Event 1'}],
                        'event_reports_1_entries': [{'id': 1, 'event_details': 'Details 1'}],
                        'event_reports': [{'id': 1, 'owner': 'User 1'}],
                        'event_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'performance_review_answer_reports_entries': [{'id': 1, 'answer': 'Answer 1'}],
                        'performance_review_answer_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'performance_review_reports_entries': [{'id': 1, 'review': 'Review 1'}],
                        'performance_review_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'project_milestone_reports_entries': [{'id': 1, 'milestone': 'Milestone 1'}],
                        'project_milestone_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'project_reports_1_entries': [{'id': 1, 'project_detail': 'Detail 1'}],
                        'project_reports_entries': [{'id': 1, 'project': 'Project 1'}],
                        'project_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'savings_reports_entries': [{'id': 1, 'savings': 100}],
                        'savings_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'supplier_reports_entries': [{'id': 1, 'supplier': 'Supplier 1'}],
                        'supplier_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'supplier_review_reports_entries': [{'id': 1, 'review': 'Good'}],
                        'supplier_review_reports_schema': {'type': 'object', 'properties': {'id': {'type': 'integer'}}},
                        'suppliers': [{'id': 1, 'name': 'Supplier A'}, {'id': 2, 'name': 'Supplier B'}]
                        },
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}

        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state('test_state.json')

    def tearDown(self):
        if os.path.exists('test_state.json'):
            os.remove('test_state.json')

    def test_contract_milestone_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.ContractMilestoneReports.get_entries(), [{'id': 1, 'name': 'Milestone 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.ContractMilestoneReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_contract_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.ContractReports.get_entries(), [{'id': 1, 'contract_name': 'Contract 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.ContractReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_event_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.EventReports.get_entries(), [{'id': 1, 'event_name': 'Event 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.EventReports.get_event_report_entries(1), [{'id': 1, 'event_details': 'Details 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.EventReports.get_reports(), [{'id': 1, 'owner': 'User 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.EventReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_performance_review_answer_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.PerformanceReviewAnswerReports.get_entries(), [{'id': 1, 'answer': 'Answer 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.PerformanceReviewAnswerReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_performance_review_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.PerformanceReviewReports.get_entries(), [{'id': 1, 'review': 'Review 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.PerformanceReviewReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_project_milestone_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.ProjectMilestoneReports.get_entries(), [{'id': 1, 'milestone': 'Milestone 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.ProjectMilestoneReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_project_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.ProjectReports.get_project_report_entries(1), [{'id': 1, 'project_detail': 'Detail 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.ProjectReports.get_entries(), [{'id': 1, 'project': 'Project 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.ProjectReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_savings_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.SavingsReports.get_entries(), [{'id': 1, 'savings': 100}])
        self.assertEqual(WorkdayStrategicSourcingAPI.SavingsReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_supplier_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.SupplierReports.get_entries(), [{'id': 1, 'supplier': 'Supplier 1'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.SupplierReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_supplier_review_reports(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.SupplierReviewReports.get_entries(), [{'id': 1, 'review': 'Good'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.SupplierReviewReports.get_schema(), {'type': 'object', 'properties': {'id': {'type': 'integer'}}})

    def test_suppliers(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.Suppliers.get_suppliers(), [{'id': 1, 'name': 'Supplier A'}, {'id': 2, 'name': 'Supplier B'}])
        self.assertEqual(WorkdayStrategicSourcingAPI.Suppliers.get_supplier(1), {'id': 1, 'name': 'Supplier A'})
        self.assertEqual(WorkdayStrategicSourcingAPI.Suppliers.get_supplier(3), None)

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]['test_key'] = 'test_value'
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state('test_state.json')
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state('test_state.json')
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["projects"]['test_key'], 'test_value')

class TestSCIMAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {
                        "payment_terms": [],
                        "payment_types": [],
                        "payment_currencies": [],
                        "payment_term_id_counter": 1,
                        "payment_type_id_counter": 1,
                        "payment_currency_id_counter": 1,
                        },
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["users"] = [{"id": "1", "name": "Test User 1"}, {"id": "2", "name": "Test User 2"}]
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["schemas"] = [{"uri": "user", "attributes": ["id", "name"]}]
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["resource_types"] = [{"resource": "users", "schema": "user"}]
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["service_provider_config"] = {"version": "1.0"}

    def test_users_get(self):
        users = WorkdayStrategicSourcingAPI.Users.get()
        self.assertEqual(len(users), 2)

    def test_users_post(self):
        new_user = WorkdayStrategicSourcingAPI.Users.post({"name": "New User"})
        self.assertEqual(new_user["id"], "3")
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["users"]), 3)

    def test_user_by_id_get(self):
        user = WorkdayStrategicSourcingAPI.UserById.get("1")
        self.assertEqual(user["name"], "Test User 1")

    def test_user_by_id_patch(self):
        WorkdayStrategicSourcingAPI.UserById.patch("1", {"Operations": [{"op": "replace", "path": "name", "value": "Updated User"}]})
        user = WorkdayStrategicSourcingAPI.UserById.get("1")
        self.assertEqual(user["name"], "Updated User")

    def test_user_by_id_put(self):
        WorkdayStrategicSourcingAPI.UserById.put("1", {"name": "Replaced User"})
        user = WorkdayStrategicSourcingAPI.UserById.get("1")
        self.assertEqual(user["name"], "Replaced User")
        self.assertEqual(user["id"],"1")

    def test_user_by_id_delete(self):
        result = WorkdayStrategicSourcingAPI.UserById.delete("1")
        self.assertTrue(result)
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["users"]), 1)

    def test_schemas_get(self):
        schemas = WorkdayStrategicSourcingAPI.Schemas.get()
        self.assertEqual(len(schemas), 1)

    def test_schema_by_id_get(self):
        schema = WorkdayStrategicSourcingAPI.SchemaById.get("user")
        self.assertEqual(schema["uri"], "user")

    def test_resource_types_get(self):
        resource_types = WorkdayStrategicSourcingAPI.ResourceTypes.get()
        self.assertEqual(len(resource_types), 1)

    def test_resource_type_by_id_get(self):
        resource_type = WorkdayStrategicSourcingAPI.ResourceTypeById.get("users")
        self.assertEqual(resource_type["resource"], "users")

    def test_service_provider_config_get(self):
        config = WorkdayStrategicSourcingAPI.ServiceProviderConfig.get()
        self.assertEqual(config["version"], "1.0")

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_state.json")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {"users": [], "schemas": [], "resource_types": [], "service_provider_config": {}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_state.json")
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["users"]), 2)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["scim"]["users"][0]["name"], "Test User 1")

class TestSpendCategoriesAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {
            'attachments': {},
            'awards': {'award_line_items': [], 'awards': []},
            'contracts': {'award_line_items': [],
                        'awards': {},
                        'contract_types': {},
                        'contracts': {}},
            'events': {'bid_line_items': {},
                        'bids': {},
                        'event_templates': {},
                        'events': {},
                        'line_items': {},
                        'worksheets': {}},
            'fields': {'field_groups': {}, 'field_options': {}, 'fields': {}},
            'payments': {
                        "payment_terms": [],
                        "payment_types": [],
                        "payment_currencies": [],
                        "payment_term_id_counter": 1,
                        "payment_type_id_counter": 1,
                        "payment_currency_id_counter": 1,
                        },
            'projects': {'project_types': {}, 'projects': {}},
            'reports': {'contract_milestone_reports_entries': [],
                        'contract_milestone_reports_schema': {},
                        'contract_reports_entries': [],
                        'contract_reports_schema': {},
                        'event_reports': [],
                        'event_reports_1_entries': [],
                        'event_reports_entries': [],
                        'event_reports_schema': {},
                        'performance_review_answer_reports_entries': [],
                        'performance_review_answer_reports_schema': {},
                        'performance_review_reports_entries': [],
                        'performance_review_reports_schema': {},
                        'project_milestone_reports_entries': [],
                        'project_milestone_reports_schema': {},
                        'project_reports_1_entries': [],
                        'project_reports_entries': [],
                        'project_reports_schema': {},
                        'savings_reports_entries': [],
                        'savings_reports_schema': {},
                        'supplier_reports_entries': [],
                        'supplier_reports_schema': {},
                        'supplier_review_reports_entries': [],
                        'supplier_review_reports_schema': {},
                        'suppliers': []},
            'scim': {'resource_types': [],
                    'schemas': [],
                    'service_provider_config': {},
                    'users': []},
            'spend_categories': {},
            'suppliers': {'contact_types': {},
                        'supplier_companies': {},
                        'supplier_company_segmentations': {},
                        'supplier_contacts': {}}}
        self.test_file = "test_state.json"

    def tearDown(self):
        import os
        try:
            os.remove(self.test_file)
        except FileNotFoundError:
            pass

    def test_get_spend_categories(self):
        self.assertEqual(WorkdayStrategicSourcingAPI.SpendCategories.get(), [])
        WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 1")
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SpendCategories.get()), 1)

    def test_post_spend_category(self):
        category = WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 2", external_id="ext-1", usages=["procurement"])
        self.assertEqual(category["name"], "Test Category 2")
        self.assertEqual(category["external_id"], "ext-1")
        self.assertEqual(category["usages"], ["procurement"])

    def test_get_spend_category_by_id(self):
        category = WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 3")
        retrieved_category = WorkdayStrategicSourcingAPI.SpendCategoryById.get(category["id"])
        self.assertEqual(retrieved_category, category)
        self.assertIsNone(WorkdayStrategicSourcingAPI.SpendCategoryById.get(999))

    def test_patch_spend_category_by_id(self):
        category = WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 4")
        updated_category = WorkdayStrategicSourcingAPI.SpendCategoryById.patch(category["id"], name="Updated Name")
        self.assertEqual(updated_category["name"], "Updated Name")
        self.assertEqual(WorkdayStrategicSourcingAPI.SpendCategoryById.get(category["id"])["name"], "Updated Name")
        self.assertIsNone(WorkdayStrategicSourcingAPI.SpendCategoryById.patch(999, name="Updated Name"))

    def test_delete_spend_category_by_id(self):
        category = WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 5")
        self.assertTrue(WorkdayStrategicSourcingAPI.SpendCategoryById.delete(category["id"]))
        self.assertIsNone(WorkdayStrategicSourcingAPI.SpendCategoryById.get(category["id"]))
        self.assertFalse(WorkdayStrategicSourcingAPI.SpendCategoryById.delete(999))

    def test_get_spend_category_by_external_id(self):
        category = WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 6", external_id="ext-2")
        retrieved_category = WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.get("ext-2")
        self.assertEqual(retrieved_category, category)
        self.assertIsNone(WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.get("ext-999"))

    def test_patch_spend_category_by_external_id(self):
        category = WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 7", external_id="ext-3")
        updated_category = WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.patch("ext-3", name="Updated Name 2")
        self.assertEqual(updated_category["name"], "Updated Name 2")
        self.assertEqual(WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.get("ext-3")["name"], "Updated Name 2")
        self.assertIsNone(WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.patch("ext-999", name="Updated Name 2"))

    def test_delete_spend_category_by_external_id(self):
        category = WorkdayStrategicSourcingAPI.SpendCategories.post(name="Test Category 8", external_id="ext-4")
        self.assertTrue(WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.delete("ext-4"))
        self.assertIsNone(WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.get("ext-4"))
        self.assertFalse(WorkdayStrategicSourcingAPI.SpendCategoryByExternalId.delete("ext-999"))

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.SpendCategories.post(name="Persistent Category", external_id="persistent-1")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state(self.test_file)
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB = {"spend_categories": {}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state(self.test_file)
        self.assertEqual(len(WorkdayStrategicSourcingAPI.SpendCategories.get()), 1)
        self.assertEqual(WorkdayStrategicSourcingAPI.SpendCategories.get()[0]["name"], "Persistent Category")
        self.assertEqual(WorkdayStrategicSourcingAPI.SpendCategories.get()[0]["external_id"], "persistent-1")

import unittest
import APIs.WorkdayStrategicSourcingAPISimulation as WorkdayStrategicSourcingAPI
import os

class TestAPI(unittest.TestCase):
    def setUp(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_state.json")
        self.maxDiff = None

    def tearDown(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_state.json")

    def test_supplier_companies_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanies.get()
        self.assertEqual(status, 200)
        self.assertEqual(result, [{"id": 1, "name": "Test Company"}])

    def test_supplier_companies_post(self):
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanies.post(body={"name": "New Company", "external_id": "ext1"})
        self.assertEqual(status, 201)
        self.assertEqual(result["name"], "New Company")
        self.assertEqual(result["external_id"], "ext1")

    def test_supplier_company_by_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyById.get(1)
        self.assertEqual(status, 200)
        self.assertEqual(result, {"id": 1, "name": "Test Company"})

    def test_supplier_company_by_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyById.patch(1, body={"name": "Updated Company"})
        self.assertEqual(status, 200)
        self.assertEqual(result["name"], "Updated Company")

    def test_supplier_company_by_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyById.delete(1)
        self.assertEqual(status, 204)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"], {})

    def test_supplier_company_by_external_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company", "external_id": "ext1"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyByExternalId.get("ext1")
        self.assertEqual(status, 200)
        self.assertEqual(result, {"id": 1, "name": "Test Company", "external_id": "ext1"})

    def test_supplier_company_by_external_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company", "external_id": "ext1"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyByExternalId.patch("ext1", body={"name": "Updated Company", "id": "ext1"})
        self.assertEqual(status, 200)
        self.assertEqual(result["name"], "Updated Company")

    def test_supplier_company_by_external_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company", "external_id": "ext1"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyByExternalId.delete("ext1")
        self.assertEqual(status, 204)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"], {})

    def test_supplier_company_contacts_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company"}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Contact 1", "company_id": 1}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyContacts.get(1)
        self.assertEqual(status, 200)
        self.assertEqual(result, [{"id": 1, "name": "Contact 1", "company_id": 1}])

    def test_supplier_companies_describe_get(self):
        result, status = WorkdayStrategicSourcingAPI.SupplierCompaniesDescribe.get()
        self.assertEqual(status, 200)
        self.assertEqual(result, ['id', 'name'])

    def test_supplier_contacts_post(self):
        result, status = WorkdayStrategicSourcingAPI.SupplierContacts.post(body={"name": "New Contact", "company_id": 1, "external_id": "cont1"})
        self.assertEqual(status, 201)
        self.assertEqual(result["name"], "New Contact")
        self.assertEqual(result["company_id"], 1)
        self.assertEqual(result["external_id"], "cont1")

    def test_supplier_contact_by_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Test Contact"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierContactById.get(1)
        self.assertEqual(status, 200)
        self.assertEqual(result, {"id": 1, "name": "Test Contact"})

    def test_supplier_contact_by_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Test Contact"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierContactById.patch(1, body={"id": 1, "name": "Updated Contact"})
        self.assertEqual(status, 200)
        self.assertEqual(result["name"], "Updated Contact")

    def test_supplier_contact_by_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Test Contact"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierContactById.delete(1)
        self.assertEqual(status, 204)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"], {})

    def test_supplier_company_contacts_by_external_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company", "external_id": "ext1"}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Contact 1", "company_id": 1}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanyContactsByExternalId.get("ext1")
        self.assertEqual(status, 200)
        self.assertEqual(result, [{"id": 1, "name": "Contact 1", "company_id": 1}])

    def test_supplier_contact_by_external_id_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Test Contact", "external_id": "cont1"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierContactByExternalId.get("cont1")
        self.assertEqual(status, 200)
        self.assertEqual(result, {"id": 1, "name": "Test Contact", "external_id": "cont1"})

    def test_supplier_contact_by_external_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Test Contact", "external_id": "cont1"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierContactByExternalId.patch(external_id="cont1", body={"name": "Updated Contact", "id":"cont1", "external_id": "cont1"})
        self.assertEqual(status, 200)
        self.assertEqual(result["name"], "Updated Contact")

    def test_supplier_contact_by_external_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"] = {1: {"id": 1, "name": "Test Contact", "external_id": "cont1"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierContactByExternalId.delete("cont1")
        self.assertEqual(status, 204)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_contacts"], {})

    def test_contact_types_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["contact_types"] = {1: {"id": 1, "name": "Type 1"}}
        result, status = WorkdayStrategicSourcingAPI.ContactTypes.get()
        self.assertEqual(status, 200)
        self.assertEqual(result, [{"id": 1, "name": "Type 1"}])

    def test_contact_types_post(self):
        result, status = WorkdayStrategicSourcingAPI.ContactTypes.post(body={"name": "New Type", "external_id": "type1"})
        self.assertEqual(status, 201)
        self.assertEqual(result["name"], "New Type")
        self.assertEqual(result["external_id"], "type1")

    def test_contact_type_by_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["contact_types"] = {1: {"id": 1, "name": "Type 1"}}
        result, status = WorkdayStrategicSourcingAPI.ContactTypeById.patch(1, body={"id": 1, "name": "Updated Type"})
        self.assertEqual(status, 200)
        self.assertEqual(result["name"], "Updated Type")

    def test_contact_type_by_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["contact_types"] = {1: {"id": 1, "name": "Type 1"}}
        result, status = WorkdayStrategicSourcingAPI.ContactTypeById.delete(1)
        self.assertEqual(status, 204)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["contact_types"], {})

    def test_contact_type_by_external_id_patch(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["contact_types"] = {1: {"id": 1, "name": "Type 1", "external_id": "type1"}}
        result, status = WorkdayStrategicSourcingAPI.ContactTypeByExternalId.patch(external_id="type1", body={"name": "Updated Type", "id": "type1", "external_id": "type1"})
        self.assertEqual(status, 200)
        self.assertEqual(result["name"], "Updated Type")

    def test_contact_type_by_external_id_delete(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["contact_types"] = {1: {"id": 1, "name": "Type 1", "external_id": "type1"}}
        result, status = WorkdayStrategicSourcingAPI.ContactTypeByExternalId.delete("type1")
        self.assertEqual(status, 204)
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["contact_types"], {})

    def test_supplier_company_segmentations_get(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_company_segmentations"] = {1: {"id": 1, "name": "Segmentation 1"}}
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanySegmentations.get()
        self.assertEqual(status, 200)
        self.assertEqual(result, [{"id": 1, "name": "Segmentation 1"}])

    def test_supplier_company_segmentations_post(self):
        result, status = WorkdayStrategicSourcingAPI.SupplierCompanySegmentations.post(body={"name": "New Segmentation", "external_id": "seg1"})
        self.assertEqual(status, 201)
        self.assertEqual(result["name"], "New Segmentation")
        self.assertEqual(result["external_id"], "seg1")

    def test_state_persistence(self):
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {1: {"id": 1, "name": "Test Company"}}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.save_state("test_persistence.json")
        WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"] = {}
        WorkdayStrategicSourcingAPI.SimulationEngine.db.load_state("test_persistence.json")
        self.assertEqual(WorkdayStrategicSourcingAPI.SimulationEngine.db.DB["suppliers"]["supplier_companies"], {"1": {"id": 1, "name": "Test Company"}})

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)