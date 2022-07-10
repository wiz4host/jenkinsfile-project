# jenkinsfile-project

withCredentials([sshUserPrivateKey(credentialsId: "yourkeyid", keyFileVariable: 'keyfile')]) {
       stage('scp-f/b') {
        sh "scp -i ${keyfile} do sth here"
       }
   }