

from django.db.models import get_models, signals

try:
    from notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        """
        Create the datea_follow notice type for sending notifications when
        events occur.
        """
        notification.create_notice_type("new_comment", "Comentarios", "nuevo comentario a un contenido que sigues")
        notification.create_notice_type("new_vote", "Apoyos", "nuevo apoyo a un contenido que sigues")
        notification.create_notice_type("new_response", "Respuestas", "nueva respuesta oficial a un aporte que sigues")
        notification.create_notice_type("new_report", "Aportes", "nuevo aporte por parte de alguien que sigues")
        notification.create_notice_type("site_message", "Anuncios/Noticias", "comunicados, anuncios y noticias")
    
    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"