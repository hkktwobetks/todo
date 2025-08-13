class NotFoundError(Exception):
    """対象が存在しないときに使うカスタム例外"""
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail
