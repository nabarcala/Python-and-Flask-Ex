
document.getElementById('overlay-click').addEventListener('click', function() {
  document.querySelector('.bg-modal').style.display = 'flex'; 
});

document.querySelector('.modal-close').addEventListener('click', function() {
  document.querySelector('.bg-modal').style.display = 'none'; 
})



// Portfolio Slider
$(document).ready(function(){
  $('.portfolio-slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 10000,
  });
});


// Get the element with id="default-open" and click on it
document.getElementById("defaultOpen").click();

function displayProjects(evt, projectName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(projectName).style.display = "block";
  evt.currentTarget.className += " active";
}



