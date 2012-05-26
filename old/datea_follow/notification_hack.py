from django.conf import settings

from django.template import Context
from django.template.loader import render_to_string
from notification.models import Notice, NoticeType, get_notification_language, LanguageStoreNotAvailable, get_formatted_messages, should_send

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, get_language, activate
from django.core.mail import send_mail

from datea_follow.models import FollowedObjectState


# Hacked version of notification send_now to track object states
def datea_follow_notification_send_now(users, label, extra_context=None, on_site=True, sender=None):
    """
    Creates a new notice.
    
    This is intended to be how other apps create new notices.
    
    notification.send(user, "friends_invite_sent", {
        "spam": "eggs",
        "foo": "bar",
    )
    
    You can pass in on_site=False to prevent the notice emitted from being
    displayed on the site.
    """
    if extra_context is None:
        extra_context = {}
    
    notice_type = NoticeType.objects.get(label=label)
    
    protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
    current_site = Site.objects.get_current()
    
    notices_url = u"%s://%s%s" % (
        protocol,
        unicode(current_site),
        reverse("notification_notices"),
    )
    
    current_language = get_language()
    
    formats = (
        "short.txt",
        "full.txt",
        "notice.html",
        "full.html",
    ) # TODO make formats configurable
    
    for user in users:
        recipients = []
        # get user language for user from language store defined in
        # NOTIFICATION_LANGUAGE_MODULE setting
        try:
            language = get_notification_language(user)
        except LanguageStoreNotAvailable:
            language = None
        
        if language is not None:
            # activate the user's language
            activate(language)
        
        # update context with user specific translations
        context = Context({
            "recipient": user,
            "sender": sender,
            "notice": ugettext(notice_type.display),
            "notices_url": notices_url,
            "current_site": current_site,
        })
        context.update(extra_context)
        
        # get prerendered format messages
        messages = get_formatted_messages(formats, label, context)
        
        # Strip newlines from subject
        subject = "".join(render_to_string("notification/email_subject.txt", {
            "message": messages["short.txt"],
        }, context).splitlines())
        
        body = render_to_string("notification/email_body.txt", {
            "message": messages["full.txt"],
        }, context)
        
        notice = Notice.objects.create(recipient=user, message=messages["notice.html"],
            notice_type=notice_type, on_site=on_site, sender=sender)
        
        FollowedObjectState.objects.create(notice=notice, content_object=context['target_object'])
        
        if should_send(user, notice_type, "1") and user.email and user.is_active: # Email
            recipients.append(user.email)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
    
    # reset environment to original language
    activate(current_language)
    