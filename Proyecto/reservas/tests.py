# reservas/tests.py

from datetime import datetime, time
from unittest.mock import Mock
from collections import Counter
from django.test import TestCase
from django.utils import timezone
from .services.disponibilidad_service import horarios_posibles_hoy, construir_reservas_disponibles
from .services.crear_reservas_service import obtener_campos

class TestLogicaDisponibilidad(TestCase):
    def test_filtra_correctamente_horarios_de_hoy(self):

        bloques_base = [time(6, 0),time(8, 0),time(10, 0), time(12, 0), time(14, 0),time(16, 0), time(18, 0)]
        zona_mock1,zona_mock2 = Mock(),Mock()
        zonas_a_procesar = [zona_mock1,zona_mock2]

        casos_de_prueba = [
            ("12M", time(12, 0), [time(14, 0), time(16, 0), time(18, 0)]),
            ("7Pm", time(19, 0), []),
            ("5AM", time(5, 0), [time(6, 0),time(8, 0),time(10, 0), time(12, 0), time(14, 0),time(16, 0), time(18, 0)])
        ]
        for nombre, hora_actual, horas_esperadas in casos_de_prueba:
            with self.subTest(nombre_del_caso=nombre):
                momento_actual = timezone.make_aware(datetime.combine(datetime.today(), hora_actual))
                resultado_lista = list(horarios_posibles_hoy(zonas_a_procesar, momento_actual, bloques_base))
                num_zonas = len(zonas_a_procesar)
                self.assertEqual(len(resultado_lista), len(horas_esperadas) * num_zonas)
                horas_resultantes = [combinacion[2] for combinacion in resultado_lista]
                conteo_resultante = Counter(horas_resultantes)
                self.assertEqual(set(conteo_resultante.keys()), set(horas_esperadas))
                for hora in horas_esperadas:
                    self.assertEqual(conteo_resultante[hora], num_zonas)

    def test_filtra_correctamente_horarios_ocupados(self):

        zona1 = Mock()
        zona1.pk = 1

        fecha_6am = timezone.make_aware(datetime(2025, 12, 1, 6, 0))
        fecha_10am = timezone.make_aware(datetime(2025, 12, 1, 10, 0))
        fecha_14pm = timezone.make_aware(datetime(2025, 12, 1, 14, 0))
        fecha_18pm = timezone.make_aware(datetime(2025, 12, 1, 18, 0))

        horarios_todos = [
            {'zona_comun': zona1, 'fecha_hora': fecha_6am},
            {'zona_comun': zona1, 'fecha_hora': fecha_10am},
            {'zona_comun': zona1, 'fecha_hora': fecha_14pm},
            {'zona_comun': zona1, 'fecha_hora': fecha_18pm},
        ]

        casos_de_prueba = [
            (
                "Caso 1: Algunos horarios ocupados",
                {(zona1.pk, fecha_6am), (zona1.pk, fecha_18pm)},
                [horarios_todos[1], horarios_todos[2]]
            ),
            (
                "Caso 2: Todos los horarios ocupados",
                {(zona1.pk, fecha_6am), (zona1.pk, fecha_10am), (zona1.pk, fecha_14pm), (zona1.pk, fecha_18pm)},
                []
            ),
            (
                "Caso 3: Ningún horario ocupado",
                set(),
                horarios_todos
            )
        ]

        for nombre, horarios_ocupados, horarios_esperados in casos_de_prueba:

            with self.subTest(nombre_del_caso=nombre):
                horarios_disponibles = construir_reservas_disponibles(horarios_todos, horarios_ocupados)

                #Listas de diccionarios a sets de tuplas
                set_resultado = {(h['zona_comun'].pk, h['fecha_hora']) for h in horarios_disponibles}
                set_esperado = {(h['zona_comun'].pk, h['fecha_hora']) for h in horarios_esperados}

                self.assertEqual(set_resultado, set_esperado)

    def test_parsea_correctamente_datos_de_request_post(self):

        casos_de_prueba = [
            (
                "Caso 1: Formato Valido",
                {
                    'zona_comun': '2',
                    'fecha_reserva': '2025-10-05',
                    'hora_reserva': '16:00'
                },
                {
                    'id_zona_comun': '2',
                    'fecha_reserva_completa': timezone.make_aware(datetime(2025, 10, 5, 16, 0))
                }
            ),
            (
                "Caso 2: Fecha Invalida",
                {
                    'zona_comun': '2',
                    'fecha_reserva': 'fecha-invalida',
                    'hora_reserva': '16:00'
                },
                None
            ),
            (
                "Caso 3: Hora Invalida",
                {
                    'zona_comun': '2',
                    'fecha_reserva': '2025-10-05',
                    'hora_reserva': 'hola'
                },
                None
            ),
            (
                "Caso 4: Id zona comun invalido",
                {
                    'zona_comun': 'hola',
                    'fecha_reserva': '2025-10-05',
                    'hora_reserva': '16:00'
                },
                None
            )
        ]

        for nombre, entrada, esperado in casos_de_prueba:
            with self.subTest(nombre_del_caso=nombre):
                request_mock = Mock()
                request_mock.POST = entrada
                resultado = obtener_campos(request_mock)
                self.assertEqual(resultado, esperado)
