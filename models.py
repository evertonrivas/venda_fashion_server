from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func,String,Integer,CHAR,DateTime,Boolean,Column,Text,DECIMAL,SmallInteger
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime,timedelta
import jwt
import bcrypt

db = SQLAlchemy()

class CmmUsers(db.Model,SerializerMixin):
    id              = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    username        = Column(String(100), nullable=False)
    password        = Column(String(255), nullable=False)
    type            = Column(CHAR(1),nullable=False,default='L',comment='A = Administrador, L = Lojista, R = Representante, V = Vendedor, U = User')
    date_created    = Column(DateTime,nullable=False,server_default=func.now())
    date_updated    = Column(DateTime,onupdate=func.now())
    active          = Column(Boolean,nullable=False,default=True)
    token           = Column(String(255),index=True,unique=True)
    token_expire    = Column(DateTime)
    is_authenticate = Column(Boolean,nullable=False,default=False)

    def hash_pwd(self,pwd:str):
        self.password = bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()
    
    def check_pwd(self,pwd:str):
        return bcrypt.checkpw(pwd,self.password.encode())

    def get_token(self,expires_in:int=7200):
        now = datetime.utcnow()
        if self.token and self.token_expire > now + timedelta(seconds=expires_in):
            return self.token

        #encode e decode por causa da diferenca de versoes do windows que pode retornar byte array ao inves de str
        self.token = jwt.encode({"username":str(self.username),"exp": (now + timedelta(seconds=expires_in)) },"VENDA_FASHION").encode().decode()
        self.token_expire = (now + timedelta(seconds=expires_in))
        return self.token

    def revoke_token(self):
        self.token_expire = datetime.utcnow() - timedelta(seconds=1)

    def logout(self):
        self.is_authenticate = False
        self.token = None

    @staticmethod
    def check_token(token):
        user = CmmUsers.query.filter(CmmUsers.token==token).first()
        if user is None or user.token_expire < datetime.utcnow():
            return None
        return user


class CmmUserEntity(db.Model,SerializerMixin):
    id_user     = Column(Integer,nullable=False,primary_key=True)
    id_entity   = Column(Integer,nullable=False,primary_key=True,default=0)
    id_consumer = Column(Integer,nullable=False,primary_key=True,default=0)


class CmmProducts(db.Model,SerializerMixin):
    id           = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    id_category  = Column(Integer,nullable=False)
    id_type      = Column(Integer,nullable=False)
    id_model     = Column(Integer,nullable=False)
    prodCode     = Column(String(50),nullable=False)
    barCode      = Column(String(128))
    refCode      = Column(String(50),nullable=False)
    name         = Column(String(255),nullable=False)
    description  = Column(String(255))
    observation  = Column(Text)
    ncm          = Column(String(50),nullable=True)
    price        = Column(DECIMAL(10,2),nullable=False)
    price_pdv    = Column(DECIMAL(10,2),nullable=True)
    measure_unit = Column(CHAR(2),nullable=False)
    structure    = Column(CHAR(1),nullable=False,default='S',comment="S = Simples, C = Composto")
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    trash        = Column(Boolean,nullable=False,default=False)


class CmmProductsImages(db.Model,SerializerMixin):
    id          = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    id_product  = Column(Integer,nullable=False)
    img_url     = Column(String(255),nullable=False)
    img_default = Column(Boolean,default=False)


class CmmProductsTypes(db.Model,SerializerMixin):
    id           = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    name         = Column(String(128),nullable=False)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    trash        = Column(Boolean,nullable=False,default=False)


class CmmProductsModels(db.Model,SerializerMixin):
    id = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    name = Column(String(255),nullable=False)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    trash        = Column(Boolean,nullable=False,default=False)


class CmmProductsCategories(db.Model,SerializerMixin):
    id           = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name         = Column(String(128),nullable=False)
    id_parent    = Column(Integer,nullable=True)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    trash        = Column(Boolean,nullable=False,default=False)


class CmmProductsGrid(db.Model,SerializerMixin):
    id           = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name         = Column(String(128))
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    trash        = Column(Boolean,nullable=False,default=False)


class CmmProductsGridDistribution(db.Model,SerializerMixin):
    id_grid    = Column(Integer,primary_key=True,nullable=False)
    color      = Column(String(10),primary_key=True,nullable=False)
    size       = Column(String(5),primary_key=True,nullable=False)
    value      = Column(Integer,nullable=False)
    is_percent = Column(Boolean,nullable=False,default=False)


class CmmLegalEntities(db.Model,SerializerMixin):
    id           = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name         = Column(String(255),nullable=False)
    instagram    = Column(String(100),nullable=True)
    taxvat       = Column(String(30),nullable=False,comment="CPF ou CNPJ no Brasil")
    state_region = Column(CHAR(2),nullable=False)
    city         = Column(String(100),nullable=False)
    postal_code  = Column(String(30),nullable=False)
    neighborhood = Column(String(150),nullable=False)
    phone        = Column(String(30),nullable=False)
    email        = Column(String(150),nullable=False)
    type         = Column(CHAR(1),nullable=False,default='C',comment="C = Customer(Cliente), R = Representative(Representante), S = Supplier(Fornecedor)")
    trash        = Column(Boolean,nullable=False,default=False)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())


class CmmTranslateColors(db.Model,SerializerMixin):
    id      = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    hexcode = Column(String(8),nullable=False)
    name    = Column(String(100),nullable=False)
    color   = Column(String(10),nullable=False)
    trash        = Column(Boolean,nullable=False,default=False)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())


class CmmTranslateSizes(db.Model,SerializerMixin):
    id        = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    size_name = Column(String(10),nullable=False)
    size      = Column(String(5),nullable=False)
    trash        = Column(Boolean,nullable=False,default=False)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())


class B2bCustomersGroup(db.Model,SerializerMixin):
    id               = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name             = Column(String(128),nullable=False)
    need_approvement = Column(Boolean,nullable=False,)
    date_created     = Column(DateTime,nullable=False,server_default=func.now())
    date_updated     = Column(DateTime,onupdate=func.now())
    trash            = Column(Boolean,nullable=False,default=False)


class B2bCustomerGroupCustomer(db.Model,SerializerMixin):
    id_group    = Column(Integer,primary_key=True)
    id_customer = Column(Integer,primary_key=True,comment="Id da tabela CmmLegalEntities quando type=C")


class B2bCustomerGroupRepresentative(db.Model,SerializerMixin):
    id_group          = Column(Integer,primary_key=True)
    id_representative = Column(Integer,primary_key=True,comment="Id da tabela CmmLegalEntities quando type=R")


class B2bOrders(db.Model,SerializerMixin):
    id                   = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    id_customer          = Column(Integer,nullable=False)
    id_payment_condition = Column(Integer,nullable=False)
    make_online          = Column(Boolean,nullable=False,default=True,comment="Os pedidos do sistema podem ser online ou offline")
    date_created         = Column(DateTime,nullable=False,server_default=func.now())
    date_updated         = Column(DateTime,onupdate=func.now())
    trash                = Column(Boolean,nullable=False,default=False)


class B2bOrdersProducts(db.Model,SerializerMixin):
    id_order   = Column(Integer,nullable=False,primary_key=True)
    id_product = Column(Integer,nullable=False,primary_key=True)
    color      = Column(String(10),primary_key=True,nullable=False)
    size       = Column(String(5),primary_key=True,nullable=False)
    quantity   = Column(Integer,nullable=False)
    price      = Column(DECIMAL(10,2),nullable=False)
    discount   = Column(DECIMAL(10,2))
    discount_percentage = Column(DECIMAL(10,2))


class B2bCartShopping(db.Model,SerializerMixin):
    id_customer = Column(Integer,primary_key=True)
    id_product  = Column(Integer,primary_key=True)
    color       = Column(String(10),primary_key=True)
    size        = Column(String(10),primary_key=True)
    quantity   = Column(Integer,nullable=False)
    price      = Column(DECIMAL(10,2),nullable=False)
    

class B2bProductStock(db.Model,SerializerMixin):
    id_product  = Column(Integer,nullable=False,primary_key=True)
    color       = Column(String(10),nullable=False,primary_key=True)
    size        = Column(String(5),nullable=False,primary_key=True)
    quantity    = Column(SmallInteger,nullable=True)
    limited     = Column(Boolean,default=False)


class B2bTablePrice(db.Model,SerializerMixin):
    id           = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    name         = Column(String(128),nullable=False)
    start_date   = Column(DateTime)
    end_date     = Column(DateTime)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    active       = Column(Boolean,nullable=False,default=True)


class B2bTablePriceProduct(db.Model,SerializerMixin):
    id_table_price = Column(Integer,nullable=False,primary_key=True)
    id_product     = Column(Integer,nullable=False,primary_key=True)
    price          = Column(DECIMAL(10,2),nullable=False,comment="Valor de Preço do Atacado")
    price_retail   = Column(DECIMAL(10,2),nullable=False,comment="Valor de Preço do Varejo")


class B2bPaymentConditions(db.Model,SerializerMixin):
    id            = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name          = Column(String(100),nullable=False)
    received_days = Column(SmallInteger,nullable=False,default=1,comment="Dias para receber o valor")
    installments  = Column(SmallInteger,nullable=False,default=1,comment="Número de parcelas")
    date_created  = Column(DateTime,nullable=False,server_default=func.now())
    date_updated  = Column(DateTime,onupdate=func.now())
    trash         = Column(Boolean,nullable=False,default=False)


class B2bBrand(db.Model,SerializerMixin):
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name = Column(String(100),nullable=False)
    date_created  = Column(DateTime,nullable=False,server_default=func.now())
    date_updated  = Column(DateTime,onupdate=func.now())
    trash         = Column(Boolean,nullable=False,default=False)


class B2bCollection(db.Model,SerializerMixin):
    id            = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    id_brand      = Column(Integer,nullable=False)
    name          = Column(String(128),nullable=False)
    date_created  = Column(DateTime,nullable=False,server_default=func.now())
    date_updated  = Column(DateTime,onupdate=func.now())
    trash         = Column(Boolean,nullable=False,default=False)


class B2bCollectionPrice(db.Model,SerializerMixin):
    id_collection  = Column(Integer,primary_key=True,nullable=False)
    id_table_price = Column(Integer,primary_key=True,nullable=False)


class CrmFunnel(db.Model,SerializerMixin):
    id           = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name         = Column(String(128),nullable=False)
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    trash        = Column(Boolean,nullable=False,default=False)


class CrmFunnelStage(db.Model,SerializerMixin):
    id           = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    id_funnel    = Column(Integer,nullable=False)
    name         = Column(String(128),nullable=False)
    order        = Column(CHAR(2),nullable=False,default='CD',comment='CD = ')
    date_created = Column(DateTime,nullable=False,server_default=func.now())
    date_updated = Column(DateTime,onupdate=func.now())
    trash        = Column(Boolean,nullable=False,default=False)


class CrmFunnelStageCustomer(db.Model,SerializerMixin):
    id_funnel_stage = Column(Integer,primary_key=True,nullable=False)
    id_customer     = Column(Integer,primary_key=True,nullable=False)
    date_created    = Column(DateTime,nullable=False,server_default=func.now())
    date_updated    = Column(DateTime,onupdate=func.now())
