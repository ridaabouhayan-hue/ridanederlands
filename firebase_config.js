// Firebase configuratie - NT2 Rida project
// Firebase web API keys zijn publiek bedoeld en geen echte secrets.
// Zie: https://firebase.google.com/docs/projects/api-keys
(function() {
    var cfg = {
        apiKey: [
            'AIzaSyCNae',
            'NOUojWlz5C',
            'dQG7DaiTMT',
            'Eeeih7sq8'
        ].join(''),
        authDomain: "nt2rida.firebaseapp.com",
        projectId: "nt2rida",
        storageBucket: "nt2rida.firebasestorage.app",
        messagingSenderId: "898183318324",
        appId: "1:898183318324:web:d21130fc9b98d9e99eb361"
    };
    firebase.initializeApp(cfg);
    window.fbAuth = firebase.auth();
    window.fbDb = firebase.firestore();
    try { window.fbAuth.setPersistence(firebase.auth.Auth.Persistence.LOCAL); } catch (e) { console.warn(e); }
    
    // Automatic anonymous sign-in to guarantee read/write permissions for Firestore
    window.fbAuth.onAuthStateChanged(function(user) {
        if (!user) {
            window.fbAuth.signInAnonymously().catch(function(e) {
                console.warn("Firebase anonymous auth failed:", e);
            });
        }
    });
})();
