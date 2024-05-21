document.addEventListener("DOMContentLoaded", function() {
  const imageContainers = document.querySelectorAll('.image-container');

  // Initially set the first image container as active
  const initialImageContainer = document.querySelector('.image-container');
  initialImageContainer.classList.add('custom-active');

  imageContainers.forEach(container => {
    container.addEventListener('click', function() {
      const mainImg = document.querySelector('.main-img');
      const clickedImg = container.querySelector('img');
      
      // Remove 'custom-active' class from all image containers
      imageContainers.forEach(container => {
        container.classList.remove('custom-active');
      });

      // Add 'custom-active' class to the clicked image container
      container.classList.add('custom-active');

      // Update main image source
      mainImg.src = clickedImg.src;
    });
  });
});





function toggleActive(element) {
    // Get all siblings of the clicked element
    var siblings = element.parentNode.children;

    // Loop through each sibling
    for (var i = 0; i < siblings.length; i++) {
      // Remove the 'active' class from each sibling
      siblings[i].classList.remove("active");
    }

    // Add the 'active' class to the clicked element
    element.classList.add("active");
  }




