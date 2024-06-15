let slideIndex = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
const slidesToShow = 5;

function updateSlidePosition() {
  const slider = document.getElementById('slider');
  const newTransform = -slideIndex * 20; // 20% for each slide to show 5 at a time
  slider.style.transform = `translateX(${newTransform}%)`;
}

function moveSlides(n) {
  slideIndex += n;
  if (slideIndex < 0) {
    slideIndex = 0;
  } else if (slideIndex > totalSlides - slidesToShow) {
    slideIndex = totalSlides - slidesToShow;
  }
  updateSlidePosition();
}

updateSlidePosition();