"""
Limitation du nombre de requêtes par adresse IP (Flask-Limiter).

Freine la force brute sur les mots de passe et l'envoi de courriels en masse
par les formulaires publics. Le stockage est en mémoire : les compteurs sont
propres à chaque processus et remis à zéro au redémarrage, ce qui suffit pour
un seul processus (mod_wsgi en mode daemon, ou un worker gunicorn).

L'adresse IP est lue dans REMOTE_ADDR. Si un proxy inverse est un jour placé
devant l'API, il faudra ajouter werkzeug.middleware.proxy_fix.ProxyFix, sinon
tous les visiteurs partageront le même compteur.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, storage_uri="memory://")

# Connexion et changement de mot de passe : force brute.
LOGIN_LIMIT = "5 per minute;30 per hour"
# Création de compte et mot de passe oublié : envoi d'un courriel à chaque appel.
ACCOUNT_EMAIL_LIMIT = "3 per hour"
# Formulaires publics de contact et d'adhésion : envoi de courriels.
PUBLIC_FORM_LIMIT = "5 per hour"
# Export Excel du catalogue entier : coûteux à produire.
EXPORT_LIMIT = "10 per hour"
