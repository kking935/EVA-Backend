from fastapi import FastAPI
import secure

MIDDLEWARE_SETTINGS = {
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
    "expose_headers": ["*"],
    "allow_origins": [
        "http://localhost",
        "http://localhost/",
        "https://localhost",
        "https://localhost/",
        "http://localhost:3000",
        "http://localhost:3000/",
        "https://localhost:3000",
        "https://localhost:3000/",
        "http://eva-ai.vercel.app",
        "http://eva-ai.vercel.app/",
        "https://eva-ai.vercel.app",
        "https://eva-ai.vercel.app/",
        "https://eva-ai.vercel.app/survey",
        "https://eva-ai.vercel.app/report"
    ]
}

SECURITY_SETTINGS = {
    # "csp": secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'"),
    "hsts": secure.StrictTransportSecurity().max_age(31536000).include_subdomains(),
    "referrer": secure.ReferrerPolicy().no_referrer(),
    "cache_value": secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate(),
    "x_frame_options": secure.XFrameOptions().deny(),
}