"""Test del proyecto"""
import unittest
from services import services

class TestValidarPassword(unittest.TestCase):
    """"""
    def test_validar_password(self):
        """"""
        self.assertEqual(services.is_valid_password("short"),False)
        self.assertEqual(services.is_valid_password("not_upper_case"),False)
        self.assertEqual(services.is_valid_password("NOT_LOWER_CASE"),False)
        self.assertEqual(services.is_valid_password("Not_Numeric"),False)
        self.assertEqual(services.is_valid_password("Have 1 Space"),False)
        self.assertEqual(services.is_valid_password("Correct_password_1"),True)

class TestValidarEmail(unittest.TestCase):
    """"""
    def test_validar_email(self):
        """"""
        self.assertEqual(services.is_valid_email("Username"),False)
        self.assertEqual(services.is_valid_email("Username@"),False)
        self.assertEqual(services.is_valid_email("Username@Email"),False)
        self.assertEqual(services.is_valid_email("Username@Email."),False)
        self.assertEqual(services.is_valid_email("Username@Email.Extention"),True)

class TestValidarCodigo(unittest.TestCase):
    """"""
    def test_validar_codigo(self):
        """"""
        self.assertEqual(services.valid_code(services.create_autetication_code(),6,4),True)
        self.assertEqual(services.valid_code(services.create_autetication_code(8,4),8,4),True)
        self.assertEqual(services.valid_code(services.create_autetication_code(8,0),8,0),True)
        self.assertEqual(services.valid_code(services.create_autetication_code(8,-1),8,0),True)
        self.assertEqual(services.valid_code(services.create_autetication_code(0,4),0,0),True)
        self.assertEqual(services.valid_code(services.create_autetication_code(0,-1),0,0),True)
        self.assertEqual(services.valid_code(services.create_autetication_code(-2,4),0,0),True)
        self.assertEqual(services.valid_code(services.create_autetication_code(-2,-3),0,0),True)

if __name__ == '__main__':
    unittest.main()
