let slideIndex = 1;
let slideTimer;
showSlides(slideIndex);
startAutoSlide();

// Set up automatic slide change every 5 seconds (5000 milliseconds)
function startAutoSlide() {
    slideTimer = setInterval(function() {
        plusSlides(1);
    }, 5000); // زمان به 5000 میلی‌ثانیه (5 ثانیه)
}

function plusSlides(n) {
    clearInterval(slideTimer);
    showSlides(slideIndex += n);
    startAutoSlide();
}

function currentSlide(n) {
    clearInterval(slideTimer);
    showSlides(slideIndex = n);
    startAutoSlide();
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active-slider", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active-slider";
}