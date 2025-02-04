pipeline {
    agent any
    
    environment {
        // Use credentials binding for Docker Hub
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_REPO = 'asaoluolalekan1'
        DOCKER_CREDS = credentials('docker-hub-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh '''
                    python3 -m pip install --user -r requirements.txt
                    python3 -m pip install --user pytest
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh 'python3 -m pytest tests/'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${DOCKER_REPO}:${imageTag} .
                    """
                }
            }
        }
        
        stage('Push to Docker Registry') {
            steps {
                script {
                    def imageTag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                    // Secure Docker login
                    sh '''
                        echo ${DOCKER_CREDS_PSW} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_CREDS_USR} --password-stdin
                    '''
                    // Push image
                    sh """
                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}:${imageTag}
                    """
                    // Cleanup: remove login credentials
                    sh 'docker logout ${DOCKER_REGISTRY}'
                }
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
            cleanWs()
            
            // Clean up Docker images
            script {
                def imageTag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
                sh """
                    docker rmi ${DOCKER_REGISTRY}/${DOCKER_REPO}:${imageTag} || true
                    docker system prune -f || true
                """
            }
        }
    }
}