pipeline {
    agent {
        docker {
            image 'maven:3-alpine' 
            args '-v /root/.m2:/root/.m2' 
        }
    }
    stages {
        
        
        stage("git pull") {
           checkout([$class: 'GitSCM',
              branches: scm.branches,
              extensions: scm.extensions + [[$class: 'CleanCheckout']],
              submoduleCfg: [], 
              userRemoteConfigs: [[credentialsId: 'github-wiz4host', url: 'git@github.com:wiz4host/scripts.git']]
            ]) 
         }
    
    
    
    
    }
}
