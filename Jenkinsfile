pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-v /workspace:/workspace -w /workspace'
        }
    }

    stages {

        stage('Parallel Jobs') {
            parallel {

                /* ==========================
                   BACKEND JOBS
                   ========================== */

                Backend: {
                    stages {

                        stage('Build Backend') {
                            steps {
                                echo "Building Backend..."
                                sh """
                                    cd backend
                                    pip install -r requirements.txt
                                    python -m py_compile \$(find . -name '*.py')
                                """
                            }
                        }

                        stage('Unit Tests Backend') {
                            steps {
                                echo "Running Backend Tests..."
                                sh """
                                    cd backend
                                    pip install pytest
                                    pytest
                                """
                            }
                        }
                    }
                },

                /* ==========================
                   FRONTEND JOBS
                   ========================== */

                Frontend: {
                    stages {

                        stage('Build Frontend') {
                            steps {
                                echo "Building Frontend (Django)..."
                                sh """
                                    cd frontend
                                    pip install -r requirements.txt
                                    python manage.py check
                                """
                            }
                        }

                        stage('Unit Tests Frontend') {
                            steps {
                                echo "Running Frontend Tests..."
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

        /* =============================
           LOG SUMMARY
           ============================= */

        stage('Log Summary') {
            steps {
                echo "🎉 Todos os builds e testes foram executados."
            }
        }

        /* =============================
           NOTIFICATION
           ============================= */

        stage('Notify') {
            steps {
                echo "📧 Enviando notificação..."
                sh """
                    cd scripts
                    python send_email.py
                """
            }
        }
    }
}

