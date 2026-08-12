import os

from application import create_application

if __name__ == "__main__":
    app = create_application()
    port = int(os.environ.get("PORT", 7860))
    use_https = os.environ.get("USE_HTTPS", "0").lower() in ("1", "true", "yes")

    if use_https:
        app.run(host="0.0.0.0", port=port, ssl_context="adhoc")
    else:
        app.run(host="0.0.0.0", port=port)

