// Minimal frontend helpers to call the FastAPI backend for signup/login and Stripe checkout
// Usage:
// - include this script on pages with signup/login forms or buy buttons
// - add class="js-signup" to signup form, class="js-login" to login form
// - add data-price-id="price_..." and class="js-buy" to buy buttons

console.log('backend-integration.js loaded');

// Import inactivity handler
import { setupInactivityDetection } from './inactivity-handler.js';

// Add global error handler
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
});

const API_BASE = 'http://localhost:8000';

async function apiPost(path, body, token) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function signup(email, password) {
  console.log('Attempting signup with:', { email });
  try {
    const response = await apiPost('/auth/signup', { email, password });
    console.log('Signup response:', response);
    return response;
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
}

export async function login(email, password) {
  console.log('Attempting login with:', { email });
  try {
    const response = await apiPost('/auth/login', { email, password });
    console.log('Login response:', response);
    return response;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

export async function createCheckout(priceId, token) {
  return apiPost('/payments/create-checkout-session', { price_id: priceId }, token);
}

// Auto-bind simple forms/buttons if present
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM Content Loaded - Setting up auth handlers');
  
  // Add click handlers to login/signup buttons
  document.querySelectorAll('.auth-submit').forEach(button => {
    button.addEventListener('click', (e) => {
      console.log('Auth button clicked:', e.target);
    });
  });
  document.querySelectorAll('form.js-signup').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = form.querySelector('input[name="email"]')?.value || document.getElementById('signup-email')?.value;
      const password = form.querySelector('input[name="password"]')?.value || document.getElementById('signup-password')?.value;
      const res = await signup(email, password);
      if (res.id) {
        alert('Signup successful! You can now log in.');
        form.reset();
      } else if (res.detail) {
        alert('Error: ' + res.detail);
      } else {
        alert('Unexpected response');
      }
    });
  });

  document.querySelectorAll('form.js-login').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = form.querySelector('input[name="email"]')?.value || document.getElementById('login-email')?.value;
      const password = form.querySelector('input[name="password"]')?.value || document.getElementById('login-password')?.value;
      const res = await login(email, password);
      if (res.access_token) {
        localStorage.setItem('qufin_token', res.access_token);
        alert('Logged in');
        // Hide login button, show logout button
        document.querySelectorAll('.login-btn').forEach(btn => btn.style.display = 'none');
        document.querySelectorAll('.logout-btn').forEach(btn => btn.style.display = 'inline-flex');
        // Setup inactivity detection
        setupInactivityDetection();
        // Optionally close modal
        document.querySelectorAll('.auth-modal').forEach(modal => modal.classList.remove('open'));
      } else if (res.detail) {
        alert('Error: ' + res.detail);
      } else {
        alert('Unexpected response');
      }
    });
  });

  // Logout button logic
  document.querySelectorAll('.logout-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      localStorage.removeItem('qufin_token');
      // Hide logout, show login
      document.querySelectorAll('.logout-btn').forEach(b => b.style.display = 'none');
      document.querySelectorAll('.login-btn').forEach(b => b.style.display = 'inline-flex');
      alert('Logged out');
    });
  });

  document.querySelectorAll('button.js-buy').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const priceId = btn.dataset.priceId;
      if (!priceId) return alert('Price id not configured on this button');
      const token = localStorage.getItem('qufin_token');
      if (!token) {
        return alert('Please log in before purchasing');
      }
      const res = await createCheckout(priceId, token);
      if (res.url) {
        window.location.href = res.url;
      } else {
        alert('Error creating checkout: ' + (res.detail || JSON.stringify(res)));
      }
    });
  });
});
