# In settings.py

# Disable Debug mode in production (should be False in production)
DEBUG = False

# Use HTTPS cookies for security
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is only sent over HTTPS
SESSION_COOKIE_SECURE = True  # Ensure session cookie is only sent over HTTPS

# Browser-side security features
SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
X_FRAME_OPTIONS = 'DENY'  # Prevent embedding of pages in iframes (Clickjacking protection)
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent browsers from guessing content type (XSS protection)

# Ensure all HTTP requests are redirected to HTTPS
SECURE_SSL_REDIRECT = True

# Cookie settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Ensure sessions expire when the browser closes
CSRF_COOKIE_HTTPONLY = True  # Ensure the CSRF cookie is accessible only via HTTP (not JavaScript)
