pipeline {
    agent {
        docker {
            image 'maven:3-alpine' 
            args '-v /root/.m2:/root/.m2'
            label 'node003'
        }
    }
    stages {
        
        stage("git pull") {
            steps{
                checkout([$class: 'GitSCM',
                   branches: scm.branches
                   extensions: scm.extensions + [[$class: 'CleanCheckout']],
                   submoduleCfg: [], 
                   userRemoteConfigs: [[credentialsId: 'github-wiz4host-UNPWD', url: 'https://github.com/wiz4host/scripts.git']]
                ]) 
            }
           
         }
    }
}
