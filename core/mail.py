# faz a renderização de um template em uma string
from django.conf import settings
# UMA classe do django que cria e-mail alternativos
from django.core.mail import EmailMultiAlternatives
# filtro do django que vai remover as tags da HTML.
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string


def send_mail_template(
    subject, template_name, context, recipients_list,
    from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False
):
    message_html = render_to_string(template_name, context)

    message_txt = striptags(message_html)

    email = EmailMultiAlternatives(
        subject=subject, body=message_txt, from_email=from_email,
        to=recipients_list
    )
    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)
