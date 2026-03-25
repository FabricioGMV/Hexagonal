from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from twilio.rest import Client 
from dotenv import load_dotenv
import random
import os


class UserService:
    # ======== MÉTODO PARA CRIAR USUÁRIO ========
    @staticmethod
    def create_user(name, cnpj, email, celular, password, status="Inativo"):        
        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=password,
            status=status
        )
        db.session.add(user)

        codigo = str(random.randint(1000, 9999))
        user.codigo_ativacao = codigo
        print(f"CÓDIGO GERADO PARA O WHATSAPP: {codigo}")
        db.session.commit()

        # ======== INTEGRAÇÃO TWILIO ========
        try:
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_=twilio_number, 
                body=f'Olá {name}! Seu código de ativação do Mini Mercado é: {codigo}',
                to=f'whatsapp:{celular}'
            )
            print(f"Mensagem enviada! SID: {message.sid}")
        except Exception as e:
            print(f"Erro ao enviar WhatsApp: {e}")

        return UserDomain(user.id, user.name, user.cnpj, user.email, user.celular, user.password)
    
    # ======== MÉTODOS PARA ATIVAÇÃO ========
    @staticmethod
    def verify_code(email, code_received):
        user = User.query.filter_by(email=email).first()
        
        if user and user.codigo_ativacao == code_received:
            user.status = "Ativo"
            user.codigo_ativacao = None
            db.session.commit()
            return True
        return False
    
    # ======== MÉTODO PARA LISTAR USUÁRIOS ========
    @staticmethod
    def get_all():
        users = User.query.all()
        
        lista_usuarios = []
        for u in users:
            lista_usuarios.append({
                "id": u.id,
                "name": u.name,
                "cnpj": u.cnpj,
                "email": u.email,
                "celular": u.celular,
                "status": u.status,
                "codigo_ativacao": u.codigo_ativacao
            })
        return lista_usuarios
    
    # ======== MÉTODO PARA ATUALIZAR USUÁRIO ========
    @staticmethod
    def update_user(user_id, new_email=None, new_celular=None, new_password=None):
        user = User.query.get(user_id)
        if not user:
            return None

        if new_email:
            user.email = new_email
        if new_password:
            user.password = new_password

        if new_celular and new_celular != user.celular:
            user.celular = new_celular
            user.status = "Inativo"
            
            codigo = str(random.randint(1000, 9999))
            user.codigo_ativacao = codigo
            print(f"NOVO CÓDIGO GERADO PARA O WHATSAPP: {codigo}")
            
            try:
                account_sid = os.getenv("TWILIO_ACCOUNT_SID")
                auth_token = os.getenv("TWILIO_AUTH_TOKEN")
                twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    from_=twilio_number, 
                    body=f'Olá {user.name}! Seu número foi atualizado. Seu NOVO código do Mini Mercado é: {codigo}',
                    to=f'whatsapp:{user.celular}'
                )
                print(f"Nova mensagem enviada! SID: {message.sid}")
            except Exception as e:
                print(f"Erro ao enviar WhatsApp na atualização: {e}")

        db.session.commit()
        return user
