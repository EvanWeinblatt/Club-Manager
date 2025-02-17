document.addEventListener("DOMContentLoaded", () => {
    const fadeSections = document.querySelectorAll(".fade-section");
  
    const options = {
      threshold: 0.1, 
    };
  
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          obs.unobserve(entry.target);
        }
      });
    }, options);
  
    fadeSections.forEach((section) => {
      observer.observe(section);
    });
  });
  
 
  