// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a nav link
document.querySelectorAll('.nav-link').forEach(n =>
  n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
  })
);

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
  });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 100) {
    navbar.style.background = 'rgba(255, 255, 255, 0.98)';
    navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
  } else {
    navbar.style.background = 'rgba(255, 255, 255, 0.95)';
    navbar.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
  }
});

// Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px',
};

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
  const animatedElements = document.querySelectorAll(
    '.skill-category, .project-card, .stat, .section-title'
  );

  animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
});

// Typing effect for hero section
function typeWriter(element, text, speed = 100) {
  let i = 0;
  element.innerHTML = '';

  function type() {
    if (i < text.length) {
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }

  type();
}

// Initialize typing effect when page loads
window.addEventListener('load', () => {
  const heroTitle = document.querySelector('.hero-content h1');
  if (heroTitle) {
    const originalText = heroTitle.textContent;
    typeWriter(heroTitle, originalText, 150);
  }
});

// Get configuration from config.js
const getConfig = () => {
  return (
    window.PORTFOLIO_CONFIG || {
      CONTACT_API_URL: 'https://9rau1nnkg3.execute-api.us-east-1.amazonaws.com/prod/contact',
      CONTACT_FORM: {
        MIN_MESSAGE_LENGTH: 10,
        MAX_MESSAGE_LENGTH: 1000,
        MAX_NAME_LENGTH: 100,
      },
      FORM_SUBMIT_TIMEOUT: 30000,
      ENABLE_ANALYTICS: true,
    }
  );
};

// Contact form handling - Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
  const contactForm = document.getElementById('contactForm');

  // Check if contact form exists on this page
  if (!contactForm) {
    console.log('Contact form not found on this page');
    return;
  }

  const config = getConfig();
  console.log('Contact form initialized with API URL:', config.CONTACT_API_URL);

  contactForm.addEventListener('submit', async e => {
    e.preventDefault();

    const formData = new FormData(contactForm);
    const name = formData.get('name').trim();
    const email = formData.get('email').trim();
    const message = formData.get('message').trim();

    // Basic validation
    if (!name || !email || !message) {
      showNotification('Please fill in all fields.', 'error');
      return;
    }

    if (!isValidEmail(email)) {
      showNotification('Please enter a valid email address.', 'error');
      return;
    }

    if (name.length > config.CONTACT_FORM.MAX_NAME_LENGTH) {
      showNotification(
        `Name must be less than ${config.CONTACT_FORM.MAX_NAME_LENGTH} characters.`,
        'error'
      );
      return;
    }

    if (message.length < config.CONTACT_FORM.MIN_MESSAGE_LENGTH) {
      showNotification(
        `Message must be at least ${config.CONTACT_FORM.MIN_MESSAGE_LENGTH} characters long.`,
        'error'
      );
      return;
    }

    if (message.length > config.CONTACT_FORM.MAX_MESSAGE_LENGTH) {
      showNotification(
        `Message must be less than ${config.CONTACT_FORM.MAX_MESSAGE_LENGTH} characters.`,
        'error'
      );
      return;
    }

    // Send form data to AWS API
    const submitButton = contactForm.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;

    try {
      // Disable form and show loading state

      submitButton.disabled = true;
      submitButton.textContent = 'Sending...';
      submitButton.classList.add('loading');
      submitButton.style.cursor = 'not-allowed';

      // Disable all form inputs
      const formInputs = contactForm.querySelectorAll('input, textarea');
      formInputs.forEach(input => (input.disabled = true));

      showNotification('Sending message...', 'info');

      // Add timeout to prevent hanging requests
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), config.FORM_SUBMIT_TIMEOUT);

      const response = await fetch(config.CONTACT_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
          email: email,
          message: message,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      const result = await response.json();

      if (response.ok) {
        showNotification(
          // eslint-disable-next-line quotes
          result.message || "Message sent successfully! I'll get back to you soon.",
          'success'
        );
        contactForm.reset();

        // Optional: Add Google Analytics event tracking
        if (config.ENABLE_ANALYTICS && typeof gtag !== 'undefined') {
          gtag('event', 'contact_form_submit', {
            event_category: 'engagement',
            event_label: 'contact_form',
          });
        }
      } else {
        // Handle API error responses
        const errorMessage = result.error || 'Failed to send message. Please try again.';
        showNotification(errorMessage, 'error');
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        showNotification('Request timed out. Please try again.', 'error');
      } else {
        console.error('Contact form error:', error);
        showNotification('Network error. Please check your connection and try again.', 'error');
      }
    } finally {
      // Re-enable form regardless of success or failure
      const submitButton = contactForm.querySelector('button[type="submit"]');
      const formInputs = contactForm.querySelectorAll('input, textarea');

      submitButton.disabled = false;
      submitButton.textContent = originalButtonText;
      submitButton.classList.remove('loading');
      submitButton.style.cursor = 'pointer';

      formInputs.forEach(input => (input.disabled = false));
    }
  });
});

// Email validation function
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Notification system
function showNotification(message, type = 'info') {
  // Remove existing notification
  const existingNotification = document.querySelector('.notification');
  if (existingNotification) {
    existingNotification.remove();
  }

  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;

  // Add styles
  notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;

  // Add notification to page
  document.body.appendChild(notification);

  // Animate in
  setTimeout(() => {
    notification.style.transform = 'translateX(0)';
  }, 100);

  // Handle close button
  const closeBtn = notification.querySelector('.notification-close');
  closeBtn.addEventListener('click', () => {
    notification.style.transform = 'translateX(400px)';
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 300);
  });

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.style.transform = 'translateX(400px)';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.remove();
        }
      }, 300);
    }
  }, 5000);
}

// Stats counter animation
function animateStats() {
  const stats = document.querySelectorAll('.stat-number');

  stats.forEach(stat => {
    const target = parseInt(stat.textContent);
    let count = 0;
    const increment = target / 50;

    const updateCount = () => {
      if (count < target) {
        count += increment;
        stat.textContent = Math.ceil(count) + '+';
        setTimeout(updateCount, 40);
      } else {
        stat.textContent = target + '+';
      }
    };

    updateCount();
  });
}

// Trigger stats animation when stats section is visible
const statsObserver = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateStats();
        statsObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.5 }
);

document.addEventListener('DOMContentLoaded', () => {
  const statsSection = document.querySelector('.stats');
  if (statsSection) {
    statsObserver.observe(statsSection);
  }
});

// Project card hover effects
document.addEventListener('DOMContentLoaded', () => {
  const projectCards = document.querySelectorAll('.project-card');

  projectCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-15px) scale(1.02)';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0) scale(1)';
    });
  });
});

// Skill items interaction
document.addEventListener('DOMContentLoaded', () => {
  const skillItems = document.querySelectorAll('.skill-item');

  skillItems.forEach(item => {
    item.addEventListener('click', () => {
      item.style.transform = 'scale(1.1)';
      setTimeout(() => {
        item.style.transform = 'scale(1)';
      }, 200);
    });
  });
});

// Add loading animation
window.addEventListener('load', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.5s ease';

  setTimeout(() => {
    document.body.style.opacity = '1';
  }, 100);
});

// Performance optimization - Lazy load background images
document.addEventListener('DOMContentLoaded', () => {
  const lazyBackgrounds = document.querySelectorAll('[data-bg]');

  const bgObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bg = entry.target.getAttribute('data-bg');
        entry.target.style.backgroundImage = `url(${bg})`;
        entry.target.removeAttribute('data-bg');
        bgObserver.unobserve(entry.target);
      }
    });
  });

  lazyBackgrounds.forEach(bg => bgObserver.observe(bg));
});

// Console message for developers
console.log(
  '%c🚀 Christopher Corbin Portfolio',
  'color: #ff9900; font-size: 20px; font-weight: bold;'
);
console.log(
  '%cBuilt with ❤️ using HTML, CSS, JavaScript and deployed on AWS S3',
  'color: #666; font-size: 12px;'
);
console.log(
  '%cInterested in the code? Check it out on GitHub!',
  'color: #146eb4; font-size: 12px;'
);
