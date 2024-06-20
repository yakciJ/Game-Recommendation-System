function openNav() {
    document.getElementById("myNav").style.width = "50%";
    var elements = document.getElementsByClassName("bg");
    for(var i=0; i<elements.length; i++) { 
    elements[i].style.opacity='20%';
    }

  }
  
  function closeNav() {
    document.getElementById("myNav").style.width = "0%";
    var elements = document.getElementsByClassName("bg");
    for(var i=0; i<elements.length; i++) { 
    elements[i].style.opacity='100%';
    }
  }
  function redirectToProductPage() {
    const searchInput = document.getElementById('searchInput').value;
    console.log(searchInput)
    window.location.href = '../../Pages/Search/search.html';
  }

  let slideRelatedContentIndex = 0;
  let slideDevGameIndex = 0;
  let slideTagGame1Index = 0;
  let slideTagGame2Index = 0;
  let slideIndex = 0;

  const slides = document.querySelectorAll('.games');
  const totalSlides = slides.length;
  const slidesToShow = 19;
  let slideName;
  function updateSlidePosition(name) {
    const slider = document.getElementById(name);
    const newTransform = slideIndex * 3.4; // 20% for each slide to show 5 at a time
    slider.style.transform = `translateX(${newTransform}%)`;
  }
  
  function moveSlides(n, name) {
    slideName = name;
    switch (name) {
      case 'relatedContent':
        slideIndex = slideRelatedContentIndex;
        break;
      case 'devGame':
        slideIndex = slideDevGameIndex;
        break;
      case 'tagGame1':
        slideIndex = slideTagGame1Index;
        break;
      case 'tagGame2':
        slideIndex = slideTagGame2Index;
        break;
      default:
        break;
    }
    slideIndex += n;
    if (slideIndex < 0) {
      slideIndex = 0;
    } else if (slideIndex > totalSlides - slidesToShow) {
      slideIndex = totalSlides - slidesToShow;
    }
    updateSlidePosition(name);
    
  }
  
  updateSlidePosition(slideName);