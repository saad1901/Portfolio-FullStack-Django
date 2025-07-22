// Enhanced Theme Toggle Functionality
const themeToggle = document.getElementById("themeToggle");
const body = document.body;

// Check for saved theme preference or default to 'dark'
const currentTheme = localStorage.getItem("theme") || "dark";
body.setAttribute("data-theme", currentTheme);

themeToggle.addEventListener("click", () => {
  const currentTheme = body.getAttribute("data-theme");
  const newTheme = currentTheme === "dark" ? "light" : "dark";

  body.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);

  // Enhanced animation for theme toggle
  themeToggle.style.transform = "scale(0.8) rotate(180deg)";
  setTimeout(() => {
    themeToggle.style.transform = "scale(1) rotate(0deg)";
  }, 200);
});

// Enhanced Mobile Navigation
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const sidebar = document.getElementById("sidebar");

mobileMenuBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  mobileMenuBtn.classList.toggle("active");

  // Prevent body scroll when sidebar is open
  if (sidebar.classList.contains("open")) {
    body.style.overflow = "hidden";
  } else {
    body.style.overflow = "auto";
  }
});

// Close sidebar when clicking outside on mobile
document.addEventListener("click", (e) => {
  if (window.innerWidth <= 1024) {
    if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
      sidebar.classList.remove("open");
      mobileMenuBtn.classList.remove("active");
      body.style.overflow = "auto";
    }
  }
});

// Enhanced Navigation Functionality
const navLinks = document.querySelectorAll(".nav-link");
const contentSections = document.querySelectorAll(".content-section");

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    const targetSection = link.getAttribute("data-section");

    // Remove active class from all nav links and sections
    navLinks.forEach((nav) => nav.classList.remove("active"));
    contentSections.forEach((section) => section.classList.remove("active"));

    // Add active class to clicked nav link and corresponding section
    link.classList.add("active");
    document.getElementById(targetSection).classList.add("active");

    // Close mobile sidebar if open
    if (window.innerWidth <= 1024) {
      sidebar.classList.remove("open");
      mobileMenuBtn.classList.remove("active");
      body.style.overflow = "auto";
    }

    // Smooth scroll to top of content
    document.querySelector(".main-content").scrollTo({
      top: 0,
      behavior: "smooth",
    });

    // Trigger animations for the new section
    triggerSectionAnimations(targetSection);
  });
});

// Enhanced Skill Bar Animation
function animateSkillBars() {
  const skillBars = document.querySelectorAll(".skill-progress");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const skillBar = entry.target;
          const width = skillBar.getAttribute("data-width");

          // Add a delay for staggered animation
          setTimeout(() => {
            skillBar.style.width = width + "%";
          }, 300);

          observer.unobserve(skillBar);
        }
      });
    },
    { threshold: 0.3 }
  );

  skillBars.forEach((bar) => observer.observe(bar));
}

// Trigger section-specific animations
function triggerSectionAnimations(sectionId) {
  if (sectionId === "resume") {
    setTimeout(() => {
      animateSkillBars();
    }, 500);
  }
}

// Initialize skill bar animation when resume section is active
const resumeSection = document.getElementById("resume");
const resumeObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateSkillBars();
        resumeObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.2 }
);

resumeObserver.observe(resumeSection);

// Simple HTML Resume Download Function
function downloadResume() {
  // Show notification that download is starting
  showNotification("Opening resume in new tab...", "info");

  // Open resume in new tab - this works reliably for all hosting platforms
  window.open("./public/Resume.pdf", "_blank");

  // Alternative: Direct download approach
  setTimeout(() => {
    try {
      const link = document.createElement("a");
      link.href = "./public/Resume.pdf";
      link.download = "Sulabh_Saluja_Resume.pdf";
      link.target = "_blank";

      // Add to DOM, click, and remove
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      showNotification("Resume download started!", "success");
    } catch (error) {
      console.log("Direct download failed, but resume opened in new tab");
    }
  }, 500);
}

// EmailJS Configuration
(function () {
  // Initialize EmailJS with your public key
  emailjs.init("QSjoX--7tQKcFtA6f");
})();

// Enhanced Contact Form Handling with EmailJS
const contactForm = document.getElementById("contactForm");

contactForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const submitBtn = contactForm.querySelector(".submit-btn");
  const originalHTML = submitBtn.innerHTML;

  // Loading state
  submitBtn.innerHTML = `
        <i class="fas fa-spinner fa-spin"></i>
        <span>Sending...</span>
    `;
  submitBtn.disabled = true;
  submitBtn.style.background = "var(--text-muted)";

  try {
    // Send email using EmailJS
    const result = await emailjs.sendForm(
      "service_zuj48fh", // Your service ID
      "template_4hd588q", // Your template ID
      contactForm
    );

    console.log("Email sent successfully:", result);

    // Success state
    submitBtn.innerHTML = `
            <i class="fas fa-check"></i>
            <span>Message Sent!</span>
        `;
    submitBtn.style.background = "var(--accent-success)";

    // Show success message
    showNotification(
      "Message sent successfully! I'll get back to you soon.",
      "success"
    );

    // Reset form after delay
    setTimeout(() => {
      submitBtn.innerHTML = originalHTML;
      submitBtn.style.background = "var(--gradient-accent)";
      submitBtn.disabled = false;
      contactForm.reset();
    }, 3000);
  } catch (error) {
    console.error("Email sending failed:", error);

    // Error state
    submitBtn.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <span>Failed to Send</span>
        `;
    submitBtn.style.background = "var(--accent-danger)";

    // Show error message
    showNotification(
      "Failed to send message. Please try again or contact me directly.",
      "error"
    );

    // Reset form after delay
    setTimeout(() => {
      submitBtn.innerHTML = originalHTML;
      submitBtn.style.background = "var(--gradient-accent)";
      submitBtn.disabled = false;
    }, 3000);
  }
});

// Notification system
function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;

  let iconClass = "fas fa-info-circle";
  let borderColor = "var(--accent-primary)";

  if (type === "success") {
    iconClass = "fas fa-check-circle";
    borderColor = "var(--accent-success)";
  } else if (type === "error") {
    iconClass = "fas fa-exclamation-triangle";
    borderColor = "var(--accent-danger)";
  }

  notification.innerHTML = `
        <i class="${iconClass}"></i>
        <span>${message}</span>
    `;

  // Add notification styles
  notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--bg-card);
        border: 1px solid ${borderColor};
        border-radius: 12px;
        padding: 1rem 1.5rem;
        box-shadow: 0 10px 30px var(--shadow-medium);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: var(--text-primary);
        font-weight: 500;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        backdrop-filter: blur(20px);
    `;

  notification.querySelector("i").style.color = borderColor;

  document.body.appendChild(notification);

  // Animate in
  setTimeout(() => {
    notification.style.transform = "translateX(0)";
  }, 100);

  // Remove after delay
  setTimeout(() => {
    notification.style.transform = "translateX(100%)";
    setTimeout(() => {
      if (document.body.contains(notification)) {
        document.body.removeChild(notification);
      }
    }, 300);
  }, 4000);
}

// Enhanced Resume Dropdown Functionality
function toggleResumeMenu() {
  const dropdown = document.getElementById("resumeDropdown");
  dropdown.classList.toggle("show");

  // Close dropdown when clicking anywhere else
  document.addEventListener("click", function closeDropdown(e) {
    if (!e.target.closest(".resume-toggle")) {
      dropdown.classList.remove("show");
      document.removeEventListener("click", closeDropdown);
    }
  });
}

// Enhanced Parallax Effects
let ticking = false;

function updateParallax() {
  const scrolled = window.pageYOffset;
  const rate = scrolled * -0.5;

  // Avatar parallax
  const avatar = document.querySelector(".avatar");
  if (avatar) {
    avatar.style.transform = `translateY(${rate * 0.1}px)`;
  }

  // Floating elements
  const floatingElements = document.querySelectorAll(
    ".skill-card, .project-card"
  );
  floatingElements.forEach((element, index) => {
    const speed = 0.02 + index * 0.01;
    element.style.transform = `translateY(${
      Math.sin(Date.now() * speed) * 2
    }px)`;
  });

  ticking = false;
}

function requestTick() {
  if (!ticking) {
    requestAnimationFrame(updateParallax);
    ticking = true;
  }
}

window.addEventListener("scroll", requestTick);

// Enhanced Typing Effect
function typeWriter(element, text, speed = 80) {
  let i = 0;
  element.innerHTML = "";
  element.style.borderRight = "2px solid var(--accent-primary)";

  function type() {
    if (i < text.length) {
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(type, speed + Math.random() * 50);
    } else {
      // Remove cursor after typing
      setTimeout(() => {
        element.style.borderRight = "none";
      }, 1000);
    }
  }

  type();
}

// Enhanced Intersection Observer for Animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const animationObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.animationPlayState = "running";
      entry.target.classList.add("animate-in");
    }
  });
}, observerOptions);

// Observe all animated elements
document
  .querySelectorAll(
    '[class*="slideInUp"], [class*="fadeInUp"], .skill-card, .contact-method, .education-item'
  )
  .forEach((el) => {
    el.style.animationPlayState = "paused";
    animationObserver.observe(el);
  });

// Performance optimization: Debounce scroll events
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Enhanced resize handler
const debouncedResize = debounce(() => {
  if (window.innerWidth > 1024) {
    sidebar.classList.remove("open");
    mobileMenuBtn.classList.remove("active");
    body.style.overflow = "auto";
  }
}, 250);

window.addEventListener("resize", debouncedResize);

// Initialize everything when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  // Initialize typing effect
  const roleElement = document.querySelector(".role");
  if (roleElement) {
    const originalText = roleElement.textContent;
    setTimeout(() => {
      typeWriter(roleElement, originalText, 100);
    }, 1000);
  }

  // Add stagger animation delays
  document.querySelectorAll(".skill-card").forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
  });

  document.querySelectorAll(".contact-method").forEach((method, index) => {
    method.style.animationDelay = `${index * 0.2}s`;
  });

  document.querySelectorAll(".contact-item").forEach((item, index) => {
    item.style.animationDelay = `${index * 0.1}s`;
  });

  // Smooth reveal animations
  const revealElements = document.querySelectorAll(
    ".section-title, .section-subtitle, .about-text, .project-card"
  );
  revealElements.forEach((el, index) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "all 0.6s ease";

    setTimeout(() => {
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    }, index * 100);
  });

  // Add loading animation to images
  document.querySelectorAll("img").forEach((img) => {
    img.style.opacity = "0";
    img.style.transition = "opacity 0.5s ease";

    img.addEventListener("load", function () {
      this.style.opacity = "1";
    });

    // If image is already loaded
    if (img.complete) {
      img.style.opacity = "1";
    }
  });
});

// Add smooth page transitions
window.addEventListener("beforeunload", () => {
  document.body.style.opacity = "0";
  document.body.style.transform = "scale(0.98)";
});

// Enhanced error handling
window.addEventListener("error", (e) => {
  console.error("An error occurred:", e.error);
});

// Add keyboard navigation
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && sidebar.classList.contains("open")) {
    sidebar.classList.remove("open");
    mobileMenuBtn.classList.remove("active");
    body.style.overflow = "auto";
  }
});

// Performance monitoring
const perfObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.entryType === "measure") {
      console.log(`${entry.name}: ${entry.duration}ms`);
    }
  }
});

if ("PerformanceObserver" in window) {
  perfObserver.observe({ entryTypes: ["measure"] });
}