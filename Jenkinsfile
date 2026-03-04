pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/Kcarlos-dev/finance-app.git'
            }
        }

        stage('Instalar dependências') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                    echo "Dependencias criadas"
                '''
            }
        }

        stage('Verificação básica') {
            steps {
                sh '''
                    echo "Verificando se o app.py compila usando o Python do venv..."
                    ./venv/bin/python -m py_compile app.py
                '''
            }
        }

        stage('Build Docker') {
            when {
                expression { fileExists('Dockerfile') }
            }
            steps {
                sh '''
                    echo "Validando build da imagem Docker..."
                    docker build -t finance-app:${BUILD_NUMBER} .
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline terminou com status: ${currentBuild.currentResult}"
        }
    }
}