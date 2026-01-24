# Security settings to ensure HSTS is enforced
SECURE_HSTS_SECONDS = 31536000  # 1 year in seconds
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Include subdomains in HSTS
SECURE_HSTS_PRELOAD = True  # Allow the site to be preloaded in browsers' HSTS lists
