# Exceptions were created to secure bot detection, bypass not required
class VerificationPageException(Exception):
    """Raised when El País shows a verification page."""
    pass


class ArticleNotFoundException(Exception):
    """Raised when article content cannot be located."""
    pass