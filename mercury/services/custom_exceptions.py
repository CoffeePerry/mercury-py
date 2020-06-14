# coding=utf-8


class HTTPException(BaseException):
    """Common base class for all http exceptions."""
    def __init__(self, *args, **kwargs):  # real signature unknown
        self.code = kwargs.get('code')
