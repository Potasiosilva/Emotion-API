import os
import subprocess
import logging
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)

def is_venv():
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def create_venv():
    logging.info("Creando entorno virtual...")
    subprocess.check_call([sys.executable, '-m', 'venv', '.venv'])

def install_requirements(pip_executable):
    logging.info("Instalando requerimientos en el entorno virtual...")
    subprocess.check_call([pip_executable, 'install', '-r', 'requirements.txt'])

def activate_venv():
    if os.name == 'nt':
        activate_script = '.venv\\Scripts\\activate'
    else:
        activate_script = '.venv/bin/activate'
    return activate_script

def check_and_run_app():
    try:
        if is_venv():
            logging.info("Estamos dentro de un entorno virtual.")
            pip_executable = sys.executable.replace('python', 'pip')
            install_requirements(pip_executable)
            logging.info("Iniciando la API...")
            subprocess.run(['python', 'api/app.py'])
        else:
            # Verificar si ya existe el entorno virtual
            if not os.path.exists('.venv'):
                create_venv()

            # Instalar los requerimientos en el entorno virtual
            pip_executable = '.venv\\Scripts\\pip' if os.name == 'nt' else '.venv/bin/pip'
            install_requirements(pip_executable)

            # Activar el entorno virtual
            activate_script = activate_venv()
            logging.info(f"Activando el entorno virtual con {activate_script}...")
            activate_command = f'{activate_script} && python api/app.py'

            # Ejecutar la API dentro del entorno virtual
            logging.info("Iniciando la API...")
            subprocess.run(activate_command, shell=True)

    except Exception as e:
        logging.error(f"Error al ejecutar la aplicación: {e}")

if __name__ == "__main__":
    check_and_run_app()
