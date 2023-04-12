from http import HTTPStatus
from flask_restx import Resource,Namespace,fields
from flask import request
from models import B2bCustomersGroup,B2bCustomerGroupCustomer,db
import json
from sqlalchemy import exc, and_
from auth import auth
from config import Config

ns_group_customer = Namespace("customer-groups",description="Operações para manipular grupos de clientes")

####################################################################################
#            INICIO DAS CLASSES QUE IRAO TRATAR OS GRUPOS DE CLIENTES.             #
####################################################################################

cstg_pag_model = ns_group_customer.model(
    "Pagination",{
        "registers": fields.Integer,
        "page": fields.Integer,
        "per_page": fields.Integer,
        "pages": fields.Integer,
        "has_next": fields.Integer
    }
)

cst_id_model = ns_group_customer.model(
    "Customers",{
        "id": fields.Integer
    }
)

cstg_model = ns_group_customer.model(
    "CustomerGroup",{
        "id": fields.Integer,
        "name": fields.String,
        "need_approval": fields.Boolean,
        "customers": fields.List(fields.Nested(cst_id_model))
    }
)

cstg_return = ns_group_customer.model(
    "CustomerGroupReturn",{
        "pagination": fields.Nested(cstg_pag_model),
        "data": fields.List(fields.Nested(cstg_model))
    }
)



@ns_group_customer.route("/")
class UserGroupsList(Resource):
    @ns_group_customer.response(HTTPStatus.OK.value,"Obtem um registro de um grupo de usuarios",cstg_return)
    @ns_group_customer.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @ns_group_customer.param("page","Número da página de registros","query",type=int,required=True)
    @ns_group_customer.param("pageSize","Número de registros por página","query",type=int,required=True,default=25)
    @ns_group_customer.param("query","Texto para busca","query")
    @auth.login_required
    def get(self):
        pag_num  =  1 if request.args.get("page") is None else int(request.args.get("page"))
        pag_size = Config.PAGINATION_SIZE.value if request.args.get("pageSize") is None else int(request.args.get("pageSize"))
        search   = "" if request.args.get("query") is None else "{}%".format(request.args.get("query"))
        list_all = False if request.args.get("list_all") is None else True

        try:
            if search=="":
                rquery = B2bCustomersGroup.query.filter(B2bCustomersGroup.trash == False).order_by(B2bCustomersGroup.name)
            else:
                rquery = B2bCustomersGroup.query.filter(and_(B2bCustomersGroup.trash == False,B2bCustomersGroup.name.like(search))).order_by(B2bCustomersGroup.name)
                
            if list_all==False:
                rquery = rquery.paginate(page=pag_num,per_page=pag_size)

                retorno = {
                    "pagination":{
                        "registers": rquery.total,
                        "page": pag_num,
                        "per_page": pag_size,
                        "pages": rquery.pages,
                        "has_next": rquery.has_next
                    },
                    "data":[{
                        "id": m.id,
                        "name": m.name,
                        "need_approval":m.need_approval,
                        "customers": self.get_customers(m.id)
                    } for m in rquery.items]
                }
            else:
                retorno =[{
                    "id": m.id,
                    "name": m.name,
                    "need_approval":m.need_approval,
                    "customers": self.get_customers(m.id)
                } for m in rquery]
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }

    def get_customers(self,id:int):
        rquery = B2bCustomerGroupCustomer.query.filter_by(id_customer = id)
        return [{
            "id": m.id_customer
        } for m in rquery.items]

    @ns_group_customer.response(HTTPStatus.OK.value,"Cria um novo grupo de um grupo de clientes")
    @ns_group_customer.response(HTTPStatus.BAD_REQUEST.value,"Falha ao criar registro")
    @ns_group_customer.doc(body=cstg_model)
    @auth.login_required
    def post(self)->int:
        try:
            req = json.dumps(request.get_json())
            grp = B2bCustomersGroup()
            grp.name = req.name
            db.session.add(grp)
            db.session.commit()

            for cst in grp.customers:
                grpc = B2bCustomerGroupCustomer()
                grpc.id_group    = grp.id
                grpc.id_customer = cst.id
                db.session.add(grpc)
                db.session.commit()

            return grp.id
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }

@ns_group_customer.route("/<int:id>")
@ns_group_customer.param("id","Id do registro")
class UserGroupApi(Resource):
    @ns_group_customer.response(HTTPStatus.OK.value,"Retorna os dados dados de um grupo de clientes")
    @ns_group_customer.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @auth.login_required
    def get(self,id:int):
        try:
            cgroup = B2bCustomersGroup.query.get(id)
            squery = B2bCustomerGroupCustomer.query.filter_by(id_customer = id)

            return {
                "id": cgroup.id,
                "name": cgroup.name,
                "need_approval": cgroup.need_approval,
                "customers": [{
                    "id": m.id_customer
                }for m in squery.items]
            }
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }
    
    @ns_group_customer.response(HTTPStatus.OK.value,"Atualiza os dados de um grupo de clientes")
    @ns_group_customer.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @ns_group_customer.doc(body=cstg_model)
    @auth.login_required
    def post(self,id:int)->bool:
        try:
            req = json.dumps(request.get_json())
            grp = B2bCustomersGroup.query.get(id)
            grp.name          = grp.name if req.name is None else req.name
            grp.need_approval = grp.need_approval if req.need_approval is None else req.need_approval
            grp.trash         = grp.trash if req.trash is None else req.trash
            db.session.commit()


            #apaga e recria os clientes dependentes
            db.session.delete(B2bCustomerGroupCustomer()).where(B2bCustomerGroupCustomer().id_group==id)
            db.session.commit()

            for it in grp.customers:
                cst = B2bCustomerGroupCustomer()
                cst.id_customer = it.id_customer
                cst.id_group    = id
                db.session.add(cst)
                db.session.commit()

            return True
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }
    
    @ns_group_customer.response(HTTPStatus.OK.value,"Exclui os dados de um grupo de clientes")
    @ns_group_customer.response(HTTPStatus.BAD_REQUEST.value,"Registro não encontrado!")
    @auth.login_required
    def delete(self,id:int)->bool:
        try:
            grp = B2bCustomersGroup.query.get(id)
            grp.trash = True
            db.session.commit()
            return True
        except exc.SQLAlchemyError as e:
            return {
                "error_code": e.code,
                "error_details": e._message(),
                "error_sql": e._sql_message()
            }