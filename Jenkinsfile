pipeline {
    agent any

    environment {
        IMAGE_NAME = "dakshish/multi-compose-flask"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git branch: 'main', url: 'https://github.com/Dakshish-Murthy/multi-compose-flask.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🛠️ Building Docker image..."
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo "🔐 Logging in to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo "📦 Pushing Docker image to Docker Hub..."
                bat "docker push %IMAGE_NAME%"
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo "🚀 Deploying using Docker Compose..."
                bat "docker-compose down"
                bat "docker-compose up -d"
            }
        }
    }

    post {
        success {
            echo '✅ Build, push, and deployment completed successfully!'
        }
        failure {
            echo '❌ Build or deployment failed! Please check the Jenkins console output for details.'
        }
    }
}
