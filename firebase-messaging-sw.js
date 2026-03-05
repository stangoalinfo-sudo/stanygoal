importScripts('https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.8.0/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyAIHbq-1xfqpSLY9u2FW3o-HBQKvqKfhkk",
    projectId: "stanygoal",
    messagingSenderId: "56324788686",
    appId: "1:56324788686:web:8cfb0a77c934865d329b9f"
});

const messaging = firebase.messaging();

// Inapokea ujumbe wakati browser imefungwa
messaging.onBackgroundMessage((payload) => {
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/favicon.ico'
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
