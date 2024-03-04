if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/static/sw.js').then(function(registration) {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
      }, function(err) {
        console.log('ServiceWorker registration failed: ', err);
      }).catch(function(err) {
        console.log(err);
      });
    });
  }
  