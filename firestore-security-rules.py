rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
     // LOCK DOWN access_logs (already configured)
    match /access_logs/{doc} {
      allow create: if request.auth.token.email == "iot-cloud-integrated-project@appspot.gserviceaccount.com";
      allow read: if request.auth != null;
      allow update, delete: if false;
    }

    // RESTRICT authorized_users access
    match /authorized_users/{doc} {
      // Pi can read
      allow get, list: if request.auth.token.email == "pi-service-account@iot-cloud-integrated-project.iam.gserviceaccount.com";
      
      // Admin (you) can read/write
      allow read, write: if request.auth.token.email == "derek.j.garcia0413@gmail.com";  // Replace with your Google account

      // Block everything else
      allow update, delete: if false;
    }
  }
}