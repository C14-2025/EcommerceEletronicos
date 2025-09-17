from sqlalchemy import Column, String, Integer, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .connect import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # 🔑 importante
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)
    telefone = Column(String, nullable=True)

    pedidos = relationship("Pedido", back_populates="usuario")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    preco = Column(DECIMAL(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False)

    itens = relationship("PedidoItem", back_populates="produto")


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(String(30), ForeignKey("usuarios.id"))
    endereco_id = Column(Integer)  # simplificação (pode criar model Endereco depois)
    data_pedido = Column(TIMESTAMP)
    status = Column(String(50), default="pendente")

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("PedidoItem", back_populates="pedido")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)


class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unit = Column(DECIMAL(10, 2), nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id", ondelete="CASCADE"))
    valor = Column(DECIMAL(10, 2), nullable=False)
    metodo = Column(String(50))
    status = Column(String(50), default="aguardando")
    data_pagamento = Column(TIMESTAMP)

    pedido = relationship("Pedido", back_populates="pagamento")