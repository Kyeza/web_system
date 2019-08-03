import weasyprint
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import get_template


class Mailer:
    """
    Send email messages helper class
    """

    def __init__(self, from_email=None):
        # TODO setup the default from email
        self.connection = mail.get_connection()
        self.from_email = from_email

    def send_messages(self, subject, body, template, to_emails, request):
        messages = self.__generate_messages(subject, body, template, to_emails, request)
        self.__send_mail(messages)

    def __send_mail(self, mail_messages):
        """
        Send email messages
        :param mail_messages:
        :return:
        """
        self.connection.open()
        self.connection.send_messages(mail_messages)
        self.connection.close()

    def __generate_messages(self, subject, body,  template, to_emails, request):
        """
        Generate email message from Django template
        :param subject: Email message subject
        :param template: Email template
        :param to_emails: to email address[es]
        :return:
        """
        messages = []
        message_template = get_template(template)
        for recipient, context in to_emails.items():
            message_content = message_template.render(context)
            html_mail = weasyprint.HTML(string=message_content, base_url=request.build_absolute_uri())
            pdf = html_mail.write_pdf(presentational_hints=True)
            message = EmailMessage(subject, body, to=[recipient], from_email=self.from_email)
            message.content_subtype = 'html'
            message.attach('payslip.pdf', pdf, 'application/pdf')
            message.mixed_subtype = 'related'
            messages.append(message)

        return messages