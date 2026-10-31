/**
 * ComplexLab - Global Application Utilities
 */

// Global Toast Notification Helper
window.showToast = function(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.25s ease';
    setTimeout(() => toast.remove(), 250);
  }, 3200);
};

// Clipboard Helper
window.copyToClipboard = async function(text) {
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
    } else {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      textarea.remove();
    }
    window.showToast('Copied to clipboard!', 'success');
  } catch (err) {
    console.error('Clipboard copy error:', err);
    window.showToast('Failed to copy to clipboard.', 'error');
  }
};

// Mobile Hamburger Navigation
document.addEventListener('DOMContentLoaded', () => {
  const mobileBtn = document.getElementById('mobileMenuBtn');
  const navLinks = document.getElementById('navLinks');

  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (!navLinks.contains(e.target) && !mobileBtn.contains(e.target) && navLinks.classList.contains('open')) {
        navLinks.classList.remove('open');
      }
    });
  }

  // Keyboard shortcut listener: '?' opens shortcuts modal
  document.addEventListener('keydown', (e) => {
    if (e.key === '?' && !['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {
      const modal = document.getElementById('shortcutsModal');
      if (modal) modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
    }
    if (e.key === 'Escape') {
      const modal = document.getElementById('shortcutsModal');
      if (modal) modal.style.display = 'none';
    }
  });
});
