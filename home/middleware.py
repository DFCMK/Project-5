import uuid
from django.utils.deprecation import MiddlewareMixin

class CSPNonceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.csp_nonce = uuid.uuid4().hex

    def process_response(self, request, response):
        if hasattr(request, 'csp_nonce'):
            nonce = request.csp_nonce
            csp_policy = (
                f"script-src 'self' 'nonce-{nonce}' "
                "https://cdn.jsdelivr.net "
                "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js "
                "https://code.jquery.com "
                "https://js.stripe.com/v3/ "
                "https://kit.fontawesome.com/1390569447.js "
                "https://cdnjs.cloudflare.com "
                "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js; "
                f"style-src 'self' 'nonce-{nonce}' "
                "https://cdn.jsdelivr.net "
                "https://fonts.googleapis.com "
                "https://project-5dk.s3.eu-north-1.amazonaws.com "
                "https://stackpath.bootstrapcdn.com "
                "https://another-stylesheet-source.com "
                "https://cdnjs.cloudflare.com "
                "https://kit.fontawesome.com/1390569447.js; "
                "img-src 'self' "
                "https://project-5dk.s3.eu-north-1.amazonaws.com "
                "https://cdnjs.cloudflare.com "
                "https://kit.fontawesome.com; "
                "font-src 'self' "
                "https://fonts.gstatic.com "
                "https://ka-f.fontawesome.com "
                "https://cdnjs.cloudflare.com "
                "https://kit.fontawesome.com/1390569447.js; "
                "connect-src 'self' "
                "https://ka-f.fontawesome.com "
                "https://api.example.com; "
                "frame-src 'self' https://js.stripe.com "
                "https://another-iframe-source.com; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "manifest-src 'self'; "
                "media-src 'self'; "
                #"report-uri /csp-report-endpoint; "
                "worker-src 'none';"
            ).format(nonce=nonce)
            response['Content-Security-Policy'] = csp_policy
        return response