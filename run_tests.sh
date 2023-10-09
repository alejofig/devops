#!/bin/bash

# Función para crear e inicializar el entorno virtual
create_virtualenv() {
    if [ ! -d "venv" ]; then
        if [[ "$OSTYPE" == "msys" ]]; then
            python -m venv venv
        else
            python3 -m venv venv
        fi
    fi
    source venv/bin/activate
}

run_database() {
    docker run --name my_postgres -e STATIC_TOKEN=330c213d-3398-44a1-963b-b22c19c8d59c -e POSTGRES_PASSWORD=example -e POSTGRES_USER=example -e POSTGRES_DB=example -p $1:5432 -d postgres
    sleep 5 # Esperar un poco para que la base de datos se levante completamente
}


cleanup() {
    echo "Cleaning up..."
    
    # Detener y eliminar el contenedor Docker
    docker stop my_postgres
    docker rm my_postgres

    echo "Cleanup complete"
}


# Ejecutar el flujo de trabajo para pruebas del sistema
echo "Running tests..."
create_virtualenv
pip install -r requirements.txt
run_database 5434
# gunicorn --bind 0.0.0.0:4000 --workers 2 run:app
# uvicorn_pid=$!
# sleep 5
#kill "$uvicorn_pid"
coverage run -m pytest tests/* -v
coverage report
deactivate
cleanup
cd ..

