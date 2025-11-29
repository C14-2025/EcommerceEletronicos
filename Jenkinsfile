pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-v /workspace:/workspace -w /workspace'
        }
    }

    stages {

        stage('Jobs de Build e Teste') {
            parallel {

                /* ============================
                   BACKEND
                ============================ */
                stage('Backend') {
                    environment {
                        DATABASE_URL = "sqlite:///./test.db"
                    }
                    stages {

                        stage('Build Backend') {
                            steps {
                                echo "Build Backend..."
                                sh """
                                    cd backend
                                    pip install -r requirements.txt
                                    python -m py_compile \$(find . -name '*.py')
                                """
                            }
                        }

                        stage('Testes Backend') {
                            steps {
                                echo "Backend Tests..."
                                sh """
                                    cd backend
                                    pip install pytest
                                    pytest
                                """
                            }
                        }
                    }
                }

                /* ============================
                   FRONTEND
                ============================ */
                stage('Frontend') {
                    stages {

                        stage('Build Frontend') {
                            steps {
                                echo "Build Frontend..."
                                sh """
                                    cd frontend
                                    pip install -r requirements.txt
                                    python manage.py check
                                """
                            }
                        }

                        stage('Testes Frontend') {
                            steps {
                                echo "Frontend Tests..."
                                sh """
                                    cd frontend
                                    pip install -r requirements.txt
                                    python manage.py test
                                """
                            }
                        }
                    }
                }
            }
        }

        stage('Log Summary') {
            steps {
                echo "Todos os builds e testes foram executados."
            }
        }

        stage('Notificacao') {
            steps {
                echo "Enviando notificação..."
                sh """
                    cd scripts
                    python send_email.py
                """
            }
        }
    }
}
