from django.http import JsonResponse


def health(request):
    """Return "ok" so we know the server is up and running."""
    return JsonResponse({"status": "ok"})
