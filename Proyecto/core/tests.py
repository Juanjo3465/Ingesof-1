"""Test del proyecto"""
import unittest
from services import services
import pytest
from main import solicitar_contrasena, validar_asunto, validar_descripcion

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

###############################
#        TEST CONTRASEÑA      #
###############################

def test_solicitar_contrasena_correcta():
    entradas = ["password123", "password123"]
    with unittest.patch("builtins.input", side_effect=entradas):
        assert solicitar_contrasena() == "password123"

def test_solicitar_contrasena_incorrecta_luego_correcta():
    entradas = ["abc", "xyz", "hola123", "hola123"]
    with unittest.patch("builtins.input", side_effect=entradas):
        assert solicitar_contrasena() == "hola123"

###############################
#        TEST ASUNTO          #
###############################

def test_validar_asunto_valido():
    assert validar_asunto("Solicitud de mantenimiento") == True

def test_validar_asunto_corto():
    assert validar_asunto("ok") == False

def test_validar_asunto_largo():
    texto = "A" * 101
    assert validar_asunto(texto) == False

def test_validar_asunto_caracteres_invalidos():
    assert validar_asunto("Error $$ sistema") == False


###############################
#      TEST DESCRIPCIÓN       #
###############################

def test_validar_descripcion_valida():
    descripcion = "Necesito reparación de la puerta del salón comunal."
    assert validar_descripcion(descripcion) == True

def test_validar_descripcion_corta():
    assert validar_descripcion("muy corto") == False

def test_validar_descripcion_larga():
    texto = "A" * 501
    assert validar_descripcion(texto) == False

def test_validar_descripcion_caracteres_invalidos():
    assert validar_descripcion("No funciona @@@ el ascensor") == False

if __name__ == '__main__':
    unittest.main()
