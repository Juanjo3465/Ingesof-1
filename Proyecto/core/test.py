import pytest
from unittest.mock import patch
from main import solicitar_contrasena, validar_asunto, validar_descripcion

###############################
#        TEST CONTRASEÑA      #
###############################

def test_solicitar_contrasena_correcta():
    entradas = ["password123", "password123"]
    with patch("builtins.input", side_effect=entradas):
        assert solicitar_contrasena() == "password123"

def test_solicitar_contrasena_incorrecta_luego_correcta():
    entradas = ["abc", "xyz", "hola123", "hola123"]
    with patch("builtins.input", side_effect=entradas):
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
