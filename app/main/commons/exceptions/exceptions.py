from werkzeug.exceptions import HTTPException
import datetime


import logging

log = logging.getLogger()


class ErrorFormat(Exception):
    def __init__(self, status, error_msg, status_code):
        self.status = status
        self.message = error_msg
        self.status_code = status_code


class InvalidPermitException(ErrorFormat):
    """
    권한 오류
    """

    def __init__(self, code=None, msg=None):
        status = "fail"
        status_code = 200
        error_msg = "permission error"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class RequiredException(ErrorFormat):
    """
    필수 값 입력 오류
    """

    def __init__(self, code=None, msg=None):
        status = "fail"
        status_code = 400
        error_msg = "required valueinput error"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class DuplicateException(ErrorFormat):
    """
    중복 값 입력 오류
    """

    def __init__(self, code=None, msg=None):

        status = "fail"
        status_code = 400
        error_msg = "Duplicate_value_input_error"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class InvalidValueException(ErrorFormat):
    """
    데이터 형식/값 오류
    """

    def __init__(self, code=None, msg=None):
        status = "fail"
        status_code = 400
        error_msg = "data_type/value error"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class NotFoundSuccessException(ErrorFormat):
    """
    탐색 오류 (성공 처리)
    """

    def __init__(self, code=None, msg=None):
        status = "success"
        status_code = 200
        error_msg = "data not found"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class NotFoundException(ErrorFormat):
    """
    탐색 오류
    """

    def __init__(self, code=None, msg=None):
        status = "fail"
        status_code = 404
        error_msg = "data not found"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class DateException(ErrorFormat):
    """
    날짜 오류
    """

    def __init__(self, code=None, msg=None):
        status = "fail"
        status_code = 400
        error_msg = "date format error"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class RuleException(ErrorFormat):
    """
    정책 불일치 오류
    """

    def __init__(self, code=None, msg=None):
        status = "fail"
        status_code = 400
        error_msg = "policy mismatched"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class AuthException(ErrorFormat):
    """
    인증 오류
    """

    def __init__(self, code=None, msg=None):
        status = "fail"
        status_code = 400
        error_msg = "auth error"

        if code:
            status_code = code

        if msg:
            error_msg = msg

        super().__init__(status, error_msg, status_code)


class InternalServerException(ErrorFormat):
    """
    서버 오류
    """

    def __init__(self, code=None, log_msg=None):
        status = "fail"
        status_code = 500
        error_msg = "관리자에게 문의하세요"

        if code:
            status_code = code

        if log_msg:
            log.info(f"error time : {datetime.datetime.now()}")
            log.info(f"{log_msg}")

        super().__init__(status, error_msg, status_code)
