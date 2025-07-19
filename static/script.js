// Modern PollCraft JavaScript

// DOM Content Loaded
document.addEventListener("DOMContentLoaded", function () {
  // Initialize all components
  initializeErrorHandling();
  initializeAnimations();
  initializeVoting();
  initializeSearch();
  initializeModals();
});

// Error/Success Message Handling
function initializeErrorHandling() {
  const closeButtons = document.querySelectorAll("#closeError, .close-message");

  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const dialogue = this.closest(".errorDialogue, .successDialogue, .alert");
      if (dialogue) {
        dialogue.style.animation = "slideOutRight 0.3s ease-in";
        setTimeout(() => {
          dialogue.remove();
        }, 300);
      }
    });
  });

  // Auto-hide messages after 5 seconds
  const messages = document.querySelectorAll(
    ".errorDialogue, .successDialogue"
  );
  messages.forEach((message) => {
    setTimeout(() => {
      if (message.parentNode) {
        message.style.animation = "slideOutRight 0.3s ease-in";
        setTimeout(() => {
          message.remove();
        }, 300);
      }
    }, 5000);
  });
}

// Animation Initialization
function initializeAnimations() {
  // Add fade-in animation to cards
  const cards = document.querySelectorAll(".modern-card, .poll-card");
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
    card.classList.add("fade-in");
  });

  // Smooth scroll for navigation links
  const navLinks = document.querySelectorAll('a[href^="#"]');
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// Enhanced Voting System
function initializeVoting() {
  const voteButtons = document.querySelectorAll(".vote-button, .poll-option");

  voteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();

      const choiceId = this.dataset.choiceId || this.dataset.id;
      const pollId = this.dataset.pollId;

      if (!choiceId) return;

      // Add loading state
      const originalContent = this.innerHTML;
      this.innerHTML = '<span class="loading-spinner"></span> Voting...';
      this.style.pointerEvents = "none";

      // Send vote via AJAX
      fetch(`/vote/${choiceId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            showMessage(data.error, "error");
            this.innerHTML = originalContent;
            this.style.pointerEvents = "auto";
          } else {
            // Update UI with vote result
            this.classList.add("voted");
            this.innerHTML = `<span class="poll-option-text">${
              this.querySelector(".poll-option-text")?.textContent ||
              originalContent
            }</span><span class="poll-option-votes">${data.votes} votes</span>`;

            // Disable all options for this poll
            const pollOptions = document.querySelectorAll(
              `[data-poll-id="${pollId}"]`
            );
            pollOptions.forEach((option) => {
              option.style.pointerEvents = "none";
              if (option !== this) {
                option.style.opacity = "0.6";
              }
            });

            showMessage("Vote recorded successfully!", "success");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          showMessage(
            "An error occurred while voting. Please try again.",
            "error"
          );
          this.innerHTML = originalContent;
          this.style.pointerEvents = "auto";
        });
    });
  });
}

// Search Functionality
function initializeSearch() {
  const searchInput = document.querySelector("#search-input, .search-input");
  if (!searchInput) return;

  let searchTimeout;

  searchInput.addEventListener("input", function () {
    clearTimeout(searchTimeout);
    const query = this.value.trim();

    searchTimeout = setTimeout(() => {
      if (query.length >= 2 || query.length === 0) {
        performSearch(query);
      }
    }, 300);
  });
}

// Perform search with visual feedback
function performSearch(query) {
  const polls = document.querySelectorAll(".poll-card, .modern-card");

  polls.forEach((poll) => {
    const title =
      poll.querySelector(".card-title, h5")?.textContent.toLowerCase() || "";
    const content = poll.textContent.toLowerCase();

    if (
      query === "" ||
      title.includes(query.toLowerCase()) ||
      content.includes(query.toLowerCase())
    ) {
      poll.style.display = "block";
      poll.style.animation = "fadeIn 0.3s ease-out";
    } else {
      poll.style.display = "none";
    }
  });

  // Show no results message if needed
  const visiblePolls = document.querySelectorAll(
    '.poll-card:not([style*="display: none"]), .modern-card:not([style*="display: none"])'
  );
  const noResultsMsg = document.querySelector(".no-results-message");

  if (visiblePolls.length === 0 && query !== "") {
    if (!noResultsMsg) {
      const message = document.createElement("div");
      message.className = "no-results-message text-center py-5";
      message.innerHTML = `
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <h4 class="text-muted">No polls found</h4>
                <p class="text-muted">Try adjusting your search terms</p>
            `;
      document.querySelector(".poll-grid, .wrapper")?.appendChild(message);
    }
  } else if (noResultsMsg) {
    noResultsMsg.remove();
  }
}

// Modal Initialization
function initializeModals() {
  // Delete confirmation modals
  const deleteButtons = document.querySelectorAll(".delete-btn, .deleteButton");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();

      const pollId = this.dataset.pollId || this.getAttribute("data-poll-id");
      const pollTitle = this.dataset.pollTitle || "this poll";

      if (
        confirm(
          `Are you sure you want to delete "${pollTitle}"? This action cannot be undone.`
        )
      ) {
        // Add loading state
        this.innerHTML = '<span class="loading-spinner"></span> Deleting...';
        this.style.pointerEvents = "none";

        // Redirect to delete URL
        window.location.href = `/delete/${pollId}/`;
      }
    });
  });
}

// Utility Functions
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function showMessage(message, type = "info") {
  const messageDiv = document.createElement("div");
  messageDiv.className = `${
    type === "error" ? "errorDialogue" : "successDialogue"
  }`;
  messageDiv.innerHTML = `
        ${message}
        <button id="closeError" class="close-message">
            <i class="fas fa-times"></i>
        </button>
    `;

  document.body.appendChild(messageDiv);

  // Initialize close button for new message
  const closeBtn = messageDiv.querySelector(".close-message");
  closeBtn.addEventListener("click", function () {
    messageDiv.style.animation = "slideOutRight 0.3s ease-in";
    setTimeout(() => {
      messageDiv.remove();
    }, 300);
  });

  // Auto-hide after 5 seconds
  setTimeout(() => {
    if (messageDiv.parentNode) {
      messageDiv.style.animation = "slideOutRight 0.3s ease-in";
      setTimeout(() => {
        messageDiv.remove();
      }, 300);
    }
  }, 5000);
}

// Add slide out animation to CSS
const style = document.createElement("style");
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
