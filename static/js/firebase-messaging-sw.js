// Scripts for firebase and firebase messaging
importScripts('https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing the generated config
const firebaseConfig = {
    apiKey: "AIzaSyDEGT1xiOH7jJ_ZY1nqL4qkeY0cozlLWH0",
    authDomain: "iberry-550e4.firebaseapp.com",
    projectId: "iberry-550e4",
    storageBucket: "iberry-550e4.appspot.com",
    messagingSenderId: "691777412350",
    appId: "1:691777412350:web:33154ee97db49bb74c99af",
    measurementId: "G-27BGEVRQ0N"
};

firebase.initializeApp(firebaseConfig);

function speak(text) {
    const utterThis = self.SpeechSynthesisUtterance(text);
  
    utterThis.onend = function (event) {
      console.log("SpeechSynthesisUtterance.onend");
    };
  
    utterThis.onerror = function (event) {
      console.log("SpeechSynthesisUtterance.onerror");
    };
  
    // const selectedOption = voiceSelect.selectedOptions[0].getAttribute("data-name");
  
    // for (let i = 0; i < voices.length; i++) {
    //   if (voices[i].name === selectedOption) {
    //     utterThis.voice = voices[i];
    //     break;
    //   }
    // }
    // console.log("The voice name", pitch.value)
    // console.log("The voice name", rate.value)
    utterThis.pitch = 1;
    utterThis.rate = 1;
    speechSynthesis.speak(utterThis);
    // synth.speak(utterThis);
}

// Retrieve firebase messaging
const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
    console.log('Received background message ', payload);

    // Check if the browser supports the SpeechSynthesis API
    const notificationTitle = payload.notification.title;
    console.log("Notification title", notificationTitle)
    const notificationOptions = {
        body: payload.notification.body,
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
    speak(notificationTitle);
});


