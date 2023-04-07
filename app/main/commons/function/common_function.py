from dateutil.relativedelta import relativedelta
import datetime
import re
import logging
import ast
import bcrypt
from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

log = logging.getLogger()


def convert_string_to_datetime(date_str, type=0):
    """ 
    def description : 문자열을 데이트 타임으로 변환 

    Parameters
    ----------
    date_str : 문자열(str)
    type : 옵션 

    Returns
    date_time : 데이트 타임(datetime)
    -------
    """
    try:
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]

        if type == 0:
            date_time = f"{year}-{month}-{day} 00:00:00"

        else:
            date_time = f"{year}-{month}-{day} 23:59:59"

        date_time = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        return date_time

    except Exception as ex:
        log.info(f" def: convert_string_to_datetime exception : {ex}")
        return None


def convert_str_to_array(array_str):
    """ 
    def description : 문자열을 배열로 변환 

    Parameters
    ----------
    array_str : 문자열(str)

    Returns
    array : 배열(list)
    -------
    """
    array = ast.literal_eval(array_str)
    return array


def convert_to_relative_path(file_path):
    """
    =======================================================================
    Def Decription          : 상대경로만 추출
    =======================================================================
    """
    cut_point = file_path.rfind('/')+1
    if cut_point > 0:
        file_path = file_path[cut_point:]

    return file_path


def convert_user_sex_code(user_sex_code):
    """ 
    def description : user_sex_code를 텍스트로 변경 

    Parameters
    ----------
    user_sex_code : 성별 코드 (str)

    Returns
    user_sex : 성별 텍스트 (str)
    -------
    """

    if user_sex_code == "M":
        user_sex = "남자"

    else:
        user_sex = "여자"

    return user_sex


def cal_kr_age(birth):
    """ 
    def description : 한국나이 계산

    Parameters
    ----------
    birth : 생년월일(str)

    Returns
    age : 나이 (int)
    -------
    """
    birth_y = int(birth[0:4])
    today_y = int(str(datetime.datetime.now().strftime('%Y-%m-%d'))[0:4])

    age = today_y - birth_y + 1
    return age


def camel_to_snake(str):
    """
    Def Decription          : camel case, snake case로 변경
    """

    lower_str = [str[0].lower()]
    for letter in str[1:]:
        if letter in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            lower_str.append('_')
            lower_str.append(letter.lower())

        else:
            lower_str.append(letter)

    return ''.join(lower_str)


def crypt_pw(requested_inst_pw):
    """ 
    def description : 패스워드 인크립셔

    Parameters
    ----------
    requested_inst_pw : 문자열(str)

    Returns
    array : 배열(list)
    -------
    """
    requested_inst_pw = requested_inst_pw.encode("utf-8")                # 입력된 패스워드를 바이트 형태로 인코딩
    password_crypt = bcrypt.hashpw(requested_inst_pw, bcrypt.gensalt())  # 암호화된 비밀번호 생성
    password_crypt = password_crypt.decode("utf-8")                      # DB에 저장할 수 있는 유니코드 문자열 형태로 디코딩
    return password_crypt


def check_pw(input_pw, db_pw):
    """ 
    def description : 패스워드 체크 

    Parameters
    ----------
    input_pw : 인풋 패스워드(str)

    Returns
    check_pw : 결과 (Boolean)
    -------
    """
    check_pw = bcrypt.checkpw(input_pw.encode("utf-8"), db_pw.encode("utf-8"))

    return check_pw


def valid_phone(phone):
    """ 
    def description : 핸드폰 번호 유효성 검사 

    Parameters
    ----------
    phone : 핸드폰 번호 (str)

    Returns
    Boolean
    -------
    """

    if phone.find('-') > 0:
        return False

    regex = r'^(01[016789]{1}|02|0[3-9]{1}[0-9]{1})[0-9]{3,4}[0-9]{4}$'
    valid = re.search(regex, phone)

    if valid:
        return True

    else:
        return False


def valid_email(email):
    """ 
    def description : 이메일 주소 유효성 검사 

    Parameters
    ----------
    phone : 핸드폰 번호 (str)

    Returns
    Boolean
    -------
    """

    regex = r'^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$'
    valid = re.search(regex, email)

    if valid:
        return True

    else:
        return False


def generate_multipart_parser(forms=None, files=None):

    parser = reqparse.RequestParser()

    if forms:
        for form in forms:
            parser.add_argument(form, type=FileStorage, location='form')

    if files:
        for file_name in files:
            parser.add_argument(file_name, type=FileStorage, location='files')

    return parser


def generate_multipart_parser_appendable(forms=None, files=None):

    parser = reqparse.RequestParser()

    if forms:
        for form in forms:
            parser.add_argument(form, type=FileStorage, location='form')

    if files:
        for file_name in files:
            parser.add_argument(file_name, type=FileStorage, location='files', action='append')

    return parser


def generate_now_date():
    """
    Def Decription          : 오늘 날짜 시간 생성
    """
    now_date = str(datetime.datetime.now())
    now_date = now_date.replace(" ", "_")
    now_date = now_date.replace("-", "_")
    now_date = now_date.replace(":", "_")
    now_date = now_date.replace(".", "_")

    return now_date


def remove_extension(file_name):
    """
    Def Decription          : 확장자 제거
    """

    cut_point = file_name.rfind('.')
    if cut_point > 0:
        file_name = file_name[:cut_point]

    return file_name


def format_request_to_time(to_time):
    """ def description : request_to_time 포멧팅

    1초를 제외하여 리턴

    Parameters : 
    to_time : 시간 포멧 (str, 00:00:00)

    Returns
    -------
    result_time : 시간 포멧 (str, 23:59:59)
    """
    hh = int(to_time[0:2])
    mm = int(to_time[3:5])
    ss = int(to_time[6:8])

    ss += - 1
    if ss < 0:
        ss = 59
        mm += -1

    if mm < 0:
        mm = 59
        hh += -1

    if hh < 0:
        hh = 23

    hh = str(hh).zfill(2)
    mm = str(mm).zfill(2)
    ss = str(ss).zfill(2)
    result_time = f"{hh}:{mm}:{ss}"

    return result_time


def format_response_to_time(to_time):
    """ def description : response_to_time 포멧팅

    1초를 추가하여 리턴

    Parameters : 
    to_time : 시간 포멧 (str, 23:59:59)


    Returns
    -------
    result_time : 시간 포멧 (str, 00:00:00)
    """
    hh = int(to_time[0:2])
    mm = int(to_time[3:5])
    ss = int(to_time[6:8])

    ss += 1
    if ss >= 60:
        ss = 0
        mm += 1

    if mm >= 60:
        mm = 0
        hh += 1

    if hh >= 24:
        hh = 0

    hh = str(hh).zfill(2)
    mm = str(mm).zfill(2)
    ss = str(ss).zfill(2)

    result_time = f"{hh}:{mm}:{ss}"
    return result_time


def add_sec(target_time, sec):
    """ def description : 타겟 시간에 초 추가

    Parameters : 
    target_time : 타겟 시간 (str, 23:59:59)
    sec : 추가할 초(int)

    Returns
    -------
    Boolean
    """
    if abs(int(sec)) >= 60:
        return False

    hh = int(target_time[0:2])
    mm = int(target_time[3:5])
    ss = int(target_time[6:8])

    ss += sec
    if sec > 0:

        if ss >= 60:
            ss = ss - 60
            mm += 1

        if mm >= 60:
            mm = mm - 60
            hh += 1

        if hh >= 24:
            hh = hh - 24

    else:

        if ss < 0:
            ss = abs(ss + 60)
            mm += -1

        if mm < 0:
            mm = abs(mm + 60)
            hh += -1

        if hh < 0:
            hh = abs(hh + 24)

    hh = str(hh).zfill(2)
    mm = str(mm).zfill(2)
    ss = str(ss).zfill(2)

    result_time = f"{hh}:{mm}:{ss}"
    return result_time


def add_min(target_time, min):

    if abs(int(min)) >= 60:
        return False

    hh = int(target_time[0:2])
    mm = int(target_time[3:5])

    mm += min
    if mm > 0:

        if mm >= 60:
            mm = mm - 60
            hh += 1

        if hh >= 24:
            hh = hh - 24

    else:

        if mm < 0:
            mm = abs(mm + 60)
            hh += -1

        if hh < 0:
            hh = abs(hh + 24)

    hh = str(hh).zfill(2)
    mm = str(mm).zfill(2)

    result_time = f"{hh}:{mm}"
    return result_time


def get_total_page_count(total_count, limit):

    if total_count % limit == 0:
        return total_count // limit

    else:
        return total_count // limit + 1
