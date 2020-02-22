import unittest
from controller_and_modules import Controller as cT, DatabaseModule as dB


class GatewayTestCases(unittest.TestCase):
    def setUp(self) -> None:
        self.user = 5879456
        self.name = "Test"
        self.last_name = "Subject"
        self.eMail = "testUser@eTest.org"
        cT.create_single_user(self.user, self.name, self.last_name, self.eMail)

    def tearDown(self) -> None:
        test_user = cT.user_by_id(self.user)
        test_vm = cT.get_vm_object(test_user.assigned_VM)
        cT.del_user(test_user)
        cT.del_vm(test_vm)

    # Test User Functions
    def test_user_created(self):
        test_user = cT.user_by_id(self.user)
        self.assertEqual(test_user.firstName, self.name)

    def test_save_user(self):
        new_name = "Testy"
        test_user = cT.user_by_id(self.user)
        test_user.firstName = new_name
        cT.save_user(test_user)
        mod_user = cT.user_by_id(self.user)
        self.assertEqual(mod_user.firstName, new_name)

    # Test VM Functions
    def test_vm_created(self):
        test_user = cT.user_by_id(self.user)
        self.assertIsNotNone(cT.get_vm_object(test_user.assigned_VM))

    @staticmethod
    def clear_db():
        for user in cT.gateway_ses.query(dB.dbUser):
            cT.gateway_ses.delete(user)
        for vm in cT.gateway_ses.query(dB.dbComputer):
            cT.gateway_ses.delete(vm)
        cT.gateway_ses.commit()
