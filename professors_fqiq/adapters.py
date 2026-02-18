from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages

class RestrictDomainSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        allowed_domain = "unmsm.edu.pe"

        email = sociallogin.account.extra_data.get("email", "").strip().lower()

        if not email.endswith(f"@{allowed_domain}"):
            messages.error(
                request,
                f"Debes iniciar sesión con un correo institucional (@{allowed_domain})."
            )
            raise ImmediateHttpResponse(redirect("home"))

