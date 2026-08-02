# Exceptions are created to mainly secure bot detection
class VerificationPageException(Exception):
    """Raised when El País shows a verification page."""
    pass


class ArticleNotFoundException(Exception):
    """Raised when article content cannot be located."""
    pass