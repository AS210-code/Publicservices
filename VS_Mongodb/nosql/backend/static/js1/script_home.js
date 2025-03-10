document.addEventListener("DOMContentLoaded", function() {
    const categoryList = document.querySelector(".category-list");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
  
    // Scroll left
    prevBtn.addEventListener("click", function() {
      categoryList.scrollBy({
        top: 0,
        left: -200,
        behavior: "smooth",
      });
    });
  
    // Scroll right
    nextBtn.addEventListener("click", function() {
      categoryList.scrollBy({
        top: 0,
        left: 200,
        behavior: "smooth",
      });
    });
  });
  