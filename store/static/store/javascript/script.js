window.addEventListener('scroll', function() {
  var logoImg = document.getElementById('logo-img');
  var scrollPosition = window.scrollY;

  if (scrollPosition > 0) {
    logoImg.src =  '/static/store/images/whiteLogosht.png';
  } else {
    logoImg.src = '/static/store/images/whiteLogo.png';
  }

});
