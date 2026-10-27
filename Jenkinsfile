
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/hasinimahi2006/skillswap.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t skillswap-app:v1 .'
            }
        }

        stage('Login and Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker tag skillswap-app:v1 %DOCKER_USER%/skillswap-app:v1
                        docker push %DOCKER_USER%/skillswap-app:v1
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl rollout status deployment/skillswap-deployment --timeout=120s'
            }
        }
    }
}
