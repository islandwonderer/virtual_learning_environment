import unittest
import Gateway as gt
import dbModels as db


class GatewayTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.user = 5879456
        self.name = "Test"
        self.last_name = "Subject"
        self.eMail = "testUser@eTest.org"
        gt.create_single_user(self.user, self.name, self.last_name, self.eMail)

    def tearDown(self) -> None:
        test_user = gt.user_by_id(self.user)
        test_vm = gt.get_vm_object(test_user.assigned_VM)
        gt.del_user(test_user)
        gt.del_vm(test_vm)

    # Test User Functions
    def test_user_created(self):
        test_user = gt.user_by_id(self.user)
        self.assertEqual(test_user.firstName, self.name)

    def test_save_user(self):
        new_name = "Testy"
        test_user = gt.user_by_id(self.user)
        test_user.firstName = new_name
        gt.save_user(test_user)
        mod_user = gt.user_by_id(self.user)
        self.assertEqual(mod_user.firstName, new_name)

    # Test VM Functions
    def test_vm_created(self):
        test_user = gt.user_by_id(self.user)
        self.assertIsNotNone(gt.get_vm_object(test_user.assigned_VM))

    @staticmethod
    def clear_db():
        for user in gt.gateway_ses.query(db.dbUser):
            gt.gateway_ses.delete(user)
        for vm in gt.gateway_ses.query(db.dbComputer):
            gt.gateway_ses.delete(vm)
        gt.gateway_ses.commit()
