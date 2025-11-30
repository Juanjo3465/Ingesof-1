"""
Sistema de Gestión de Asambleas - Backend Flask
Adaptado para MyBuildingApp
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# ============================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'MyBuildingApp'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    """Crear conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return None

# ============================================
# RUTAS DE SALUD Y VERIFICACIÓN
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado del servidor y conexión a BD"""
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            conn.close()
            return jsonify({
                'success': True,
                'message': 'Servidor funcionando correctamente',
                'database': 'Conectada'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error de conexión a la base de datos'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============================================
# RUTAS DE ASAMBLEAS
# ============================================

@app.route('/api/asambleas', methods=['GET'])
def get_asambleas():
    """Obtener todas las asambleas o filtrar por próximas"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor(dictionary=True)
        
        # Verificar si se solicitan solo próximas asambleas
        proximas = request.args.get('proximas', 'false').lower() == 'true'
        
        if proximas:
            query = """
                SELECT * FROM Asamblea 
                WHERE fecha_hora >= NOW() 
                ORDER BY fecha_hora ASC
            """
        else:
            query = "SELECT * FROM Asamblea ORDER BY fecha_hora DESC"
        
        cursor.execute(query)
        asambleas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'asambleas': asambleas,
            'total': len(asambleas)
        }), 200
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener asambleas: {str(e)}'
        }), 500

@app.route('/api/asambleas/<int:id>', methods=['GET'])
def get_asamblea(id):
    """Obtener detalle de una asamblea específica"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM Asamblea WHERE id_asamblea = %s"
        cursor.execute(query, (id,))
        asamblea = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if asamblea:
            return jsonify({
                'success': True,
                'asamblea': asamblea
            }), 200
        else:
            return jsonify({
                'success': False,
                'mensaje': 'Asamblea no encontrada'
            }), 404
            
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener la asamblea: {str(e)}'
        }), 500

@app.route('/api/asambleas', methods=['POST'])
def create_asamblea():
    """Crear una nueva asamblea"""
    try:
        data = request.get_json()
        
        # Validación de campos requeridos
        required_fields = ['nombre', 'lugar', 'fecha_hora', 'descripcion']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'mensaje': f'El campo {field} es requerido'
                }), 400
        
        # Validaciones adicionales
        if len(data['nombre']) < 5:
            return jsonify({
                'success': False,
                'mensaje': 'El nombre debe tener al menos 5 caracteres'
            }), 400
        
        if len(data['descripcion']) < 20:
            return jsonify({
                'success': False,
                'mensaje': 'La descripción debe tener al menos 20 caracteres'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor()
        
        query = """
            INSERT INTO Asamblea 
            (nombre, lugar, fecha_hora, descripcion, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        values = (
            data['nombre'],
            data['lugar'],
            data['fecha_hora'],
            data['descripcion'],
            data.get('estado', 'Programada')
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        asamblea_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'mensaje': '✅ Asamblea creada exitosamente',
            'id_asamblea': asamblea_id
        }), 201
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al crear la asamblea: {str(e)}'
        }), 500

@app.route('/api/asambleas/<int:id>', methods=['PUT'])
def update_asamblea(id):
    """Actualizar una asamblea existente"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor()
        
        # Construir query dinámicamente según campos enviados
        fields = []
        values = []
        
        if 'nombre' in data:
            fields.append("nombre = %s")
            values.append(data['nombre'])
        if 'lugar' in data:
            fields.append("lugar = %s")
            values.append(data['lugar'])
        if 'fecha_hora' in data:
            fields.append("fecha_hora = %s")
            values.append(data['fecha_hora'])
        if 'descripcion' in data:
            fields.append("descripcion = %s")
            values.append(data['descripcion'])
        if 'estado' in data:
            fields.append("estado = %s")
            values.append(data['estado'])
        
        if not fields:
            return jsonify({
                'success': False,
                'mensaje': 'No hay campos para actualizar'
            }), 400
        
        values.append(id)
        query = f"UPDATE Asamblea SET {', '.join(fields)} WHERE id_asamblea = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'mensaje': 'Asamblea no encontrada'
            }), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'mensaje': 'Asamblea actualizada exitosamente'
        }), 200
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al actualizar la asamblea: {str(e)}'
        }), 500

@app.route('/api/asambleas/<int:id>', methods=['DELETE'])
def delete_asamblea(id):
    """Eliminar una asamblea"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor()
        
        query = "DELETE FROM Asamblea WHERE id_asamblea = %s"
        cursor.execute(query, (id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'mensaje': 'Asamblea no encontrada'
            }), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'mensaje': 'Asamblea eliminada exitosamente'
        }), 200
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al eliminar la asamblea: {str(e)}'
        }), 500

# ============================================
# RUTAS DE PETICIONES
# ============================================

@app.route('/api/peticiones', methods=['POST'])
def create_peticion():
    """Crear una nueva petición"""
    try:
        data = request.get_json()
        
        # Validación de campos requeridos
        required_fields = ['asunto', 'descripcion', 'id_asamblea', 'id_propietario']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'mensaje': f'El campo {field} es requerido'
                }), 400
        
        # Validaciones
        if len(data['asunto']) < 5:
            return jsonify({
                'success': False,
                'mensaje': 'El asunto debe tener al menos 5 caracteres'
            }), 400
        
        if len(data['descripcion']) < 20:
            return jsonify({
                'success': False,
                'mensaje': 'La descripción debe tener al menos 20 caracteres'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor()
        
        query = """
            INSERT INTO Peticion 
            (asunto, descripcion, id_asamblea, id_propietario, fecha_peticion, estado)
            VALUES (%s, %s, %s, %s, NOW(), 'Pendiente')
        """
        
        values = (
            data['asunto'],
            data['descripcion'],
            data['id_asamblea'],
            data['id_propietario']
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        peticion_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'mensaje': '✅ Petición enviada exitosamente',
            'id_peticion': peticion_id
        }), 201
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al crear la petición: {str(e)}'
        }), 500

@app.route('/api/peticiones', methods=['GET'])
def get_peticiones():
    """Obtener todas las peticiones o filtrar por asamblea"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor(dictionary=True)
        
        id_asamblea = request.args.get('id_asamblea')
        
        if id_asamblea:
            query = """
                SELECT p.*, u.nombre as nombre_propietario 
                FROM Peticion p
                LEFT JOIN Usuario u ON p.id_propietario = u.id_usuario
                WHERE p.id_asamblea = %s
                ORDER BY p.fecha_peticion DESC
            """
            cursor.execute(query, (id_asamblea,))
        else:
            query = """
                SELECT p.*, u.nombre as nombre_propietario 
                FROM Peticion p
                LEFT JOIN Usuario u ON p.id_propietario = u.id_usuario
                ORDER BY p.fecha_peticion DESC
            """
            cursor.execute(query)
        
        peticiones = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'peticiones': peticiones
        }), 200
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener peticiones: {str(e)}'
        }), 500

# ============================================
# RUTAS DE DELEGADOS
# ============================================

@app.route('/api/delegados', methods=['POST'])
def create_delegado():
    """Registrar un delegado para una asamblea"""
    try:
        data = request.get_json()
        
        # Validación de campos requeridos
        required_fields = ['id_propietario', 'id_asamblea', 'cedula', 'nombre']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'mensaje': f'El campo {field} es requerido'
                }), 400
        
        # Validaciones
        if len(str(data['cedula'])) < 6 or len(str(data['cedula'])) > 10:
            return jsonify({
                'success': False,
                'mensaje': 'La cédula debe tener entre 6 y 10 dígitos'
            }), 400
        
        if len(data['nombre']) < 3:
            return jsonify({
                'success': False,
                'mensaje': 'El nombre debe tener al menos 3 caracteres'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor()
        
        # Verificar si ya existe un delegado para este propietario en esta asamblea
        check_query = """
            SELECT id_propietario FROM Delegado 
            WHERE id_propietario = %s AND id_asamblea = %s
        """
        cursor.execute(check_query, (data['id_propietario'], data['id_asamblea']))
        existing = cursor.fetchone()
        
        if existing:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'mensaje': 'Ya has registrado un delegado para esta asamblea'
            }), 400
        
        # Insertar delegado
        query = """
            INSERT INTO Delegado 
            (id_propietario, id_asamblea, cedula, nombre)
            VALUES (%s, %s, %s, %s)
        """
        
        values = (
            data['id_propietario'],
            data['id_asamblea'],
            data['cedula'],
            data['nombre']
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'mensaje': '✅ Delegado registrado exitosamente'
        }), 201
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al registrar delegado: {str(e)}'
        }), 500

# ============================================
# RUTAS DE PARTICIPANTES
# ============================================

@app.route('/api/asambleas/<int:id>/participantes', methods=['GET'])
def get_participantes(id):
    """Obtener participantes de una asamblea (propietarios + delegados)"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'mensaje': 'Error de conexión a la base de datos'
            }), 500

        cursor = conn.cursor(dictionary=True)
        
        # Obtener propietarios (usuarios con rol Propietario)
        query_propietarios = """
            SELECT u.id_usuario, u.nombre, 
                   GROUP_CONCAT(CONCAT('Torre ', a.torre, ' - Apto ', a.numero) SEPARATOR ', ') as apartamentos
            FROM Usuario u
            LEFT JOIN Apartamentos a ON u.id_usuario = a.id_propietario
            WHERE u.rol = 'Propietario'
            GROUP BY u.id_usuario, u.nombre
        """
        cursor.execute(query_propietarios)
        propietarios = cursor.fetchall()
        
        # Obtener delegados de esta asamblea específica
        query_delegados = """
            SELECT d.cedula, d.nombre as nombre_delegado,
                   u.nombre as nombre_propietario
            FROM Delegado d
            JOIN Usuario u ON d.id_propietario = u.id_usuario
            WHERE d.id_asamblea = %s
        """
        cursor.execute(query_delegados, (id,))
        delegados = cursor.fetchall()
        
        # Calcular estadísticas
        total_propietarios = len(propietarios)
        total_delegados = len(delegados)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'propietarios_presentes': propietarios,
            'delegados': delegados,
            'estadisticas': {
                'total_propietarios': total_propietarios,
                'propietarios_presentes': total_propietarios,
                'total_delegados': total_delegados,
                'total_participantes': total_propietarios + total_delegados
            }
        }), 200
        
    except Error as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener participantes: {str(e)}'
        }), 500

# ============================================
# MANEJO DE ERRORES
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'mensaje': 'Ruta no encontrada'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'mensaje': 'Error interno del servidor'
    }), 500

# ============================================
# INICIAR SERVIDOR
# ============================================

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Iniciando servidor Flask...")
    print("=" * 50)
    print(f"📍 Host: {os.getenv('FLASK_HOST', 'localhost')}")
    print(f"🔌 Puerto: {os.getenv('FLASK_PORT', 5001)}")
    print(f"🗄️  Base de datos: {DB_CONFIG['database']}")
    print("=" * 50)
    
    app.run(
        host=os.getenv('FLASK_HOST', 'localhost'),
        port=int(os.getenv('FLASK_PORT', 5001)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )