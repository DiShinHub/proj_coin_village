from .. import db


class SampleModel(db.Model):
    """
    =======================================================================
    Table Info
    의사 등록 정보

    =====================================================
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)    # pk
    user_id = db.Column(db.String(50), nullable=False)                                  # 의사 ID
    user_pw = db.Column(db.String(255), nullable=False)                                 # 의사 패스워드
    sample_text = db.Column(db.Text, nullable=True)                                     # 의사 약력
    use_yn = db.Column(db.String(1), nullable=False)                                    # 사용 유무
    reg_dtm = db.Column(db.DateTime, nullable=False)
    mdfy_dtm = db.Column(db.DateTime, nullable=True)

