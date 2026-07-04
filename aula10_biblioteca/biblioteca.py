
from datetime import datetime, timedelta

# ============================================================
# CLASSE BASE E SUBCLASSES
# ============================================================
class ItemBiblioteca:
    """Classe base para todos os itens do acervo"""
    def __init__(self, titulo, autor, ano):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self._emprestado = False

    @property
    def emprestado(self):
        return self._emprestado

    def emprestar(self):
        if self._emprestado:
            return False
        self._emprestado = True
        return True

    def devolver(self):
        self._emprestado = False

    def calcular_multa(self, dias_atraso):
        raise NotImplementedError("Subclasses devem implementar")

    def __str__(self):
        status = "📕 Emprestado" if self._emprestado else "📗 Disponível"
        return f"{status} | '{self.titulo}' por {self.autor} ({self.ano})"

    def __eq__(self, outro):
        if isinstance(outro, ItemBiblioteca):
            return self.titulo == outro.titulo and self.autor == outro.autor
        return False


class Livro(ItemBiblioteca):
    def __init__(self, titulo, autor, ano, paginas, isbn):
        super().__init__(titulo, autor, ano)
        self.paginas = paginas
        self.isbn = isbn

    def calcular_multa(self, dias_atraso):
        return dias_atraso * 2.00

    def __str__(self):
        base = super().__str__()
        return f"{base} | {self.paginas} págs | ISBN: {self.isbn}"


class Revista(ItemBiblioteca):
    def __init__(self, titulo, autor, ano, edicao):
        super().__init__(titulo, autor, ano)
        self.edicao = edicao

    def calcular_multa(self, dias_atraso):
        return dias_atraso * 1.00

    def __str__(self):
        base = super().__str__()
        return f"{base} | Edição {self.edicao}"


class DVD(ItemBiblioteca):
    def __init__(self, titulo, autor, ano, duracao_min):
        super().__init__(titulo, autor, ano)
        self.duracao_min = duracao_min

    def calcular_multa(self, dias_atraso):
        return dias_atraso * 5.00

    def __str__(self):
        base = super().__str__()
        return f"{base} | {self.duracao_min} min"


# ============================================================
# USUÁRIO
# ============================================================
class Usuario:
    def __init__(self, nome, email, matricula):
        self.nome = nome
        self._email = None
        self.email = email
        self.matricula = matricula
        self.emprestimos = []   # lista de (ItemBiblioteca, data_emprestimo)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if '@' not in valor:
            raise ValueError("Email inválido")
        self._email = valor.lower()

    @property
    def itens_emprestados(self):
        return len(self.emprestimos)

    def __str__(self):
        return f"👤 {self.nome} ({self.matricula}) — {self.itens_emprestados} itens"

    def __eq__(self, outro):
        if isinstance(outro, Usuario):
            return self.matricula == outro.matricula
        return False


# ============================================================
# BIBLIOTECA (GERENCIADOR PRINCIPAL)
# ============================================================
class Biblioteca:
    def __init__(self, nome):
        self.nome = nome
        self._acervo = []       # lista de ItemBiblioteca
        self._usuarios = []     # lista de Usuario
        self._emprestimos = []  # lista de (usuario, item, data)

    # --- Métodos de acervo ---
    def adicionar_item(self, item):
        self._acervo.append(item)
        print(f"✅ Adicionado: {item.titulo}")

    def buscar_por_titulo(self, termo):
        resultados = [item for item in self._acervo
                      if termo.lower() in item.titulo.lower()]
        return resultados

    def listar_disponiveis(self):
        return [item for item in self._acervo if not item.emprestado]

    def listar_todos(self):
        return self._acervo

    # --- Métodos de usuário ---
    def cadastrar_usuario(self, usuario):
        if usuario in self._usuarios:
            print(f"❌ Usuário {usuario.matricula} já cadastrado.")
            return False
        self._usuarios.append(usuario)
        print(f"✅ Usuário cadastrado: {usuario.nome}")
        return True

    def buscar_usuario(self, matricula):
        for usuario in self._usuarios:
            if usuario.matricula == matricula:
                return usuario
        return None

    # --- Métodos de empréstimo ---
    def emprestar(self, matricula, titulo):
        usuario = self.buscar_usuario(matricula)
        if not usuario:
            print(f"❌ Usuário {matricula} não encontrado.")
            return False

        # Busca o item pelo título
        for item in self._acervo:
            if item.titulo.lower() == titulo.lower():
                if item.emprestado:
                    print(f"❌ '{item.titulo}' já está emprestado.")
                    return False

                if item.emprestar():
                    usuario.emprestimos.append((item, datetime.now()))
                    self._emprestimos.append((usuario, item, datetime.now()))
                    print(f"✅ '{item.titulo}' emprestado para {usuario.nome}.")
                    return True

        print(f"❌ Item '{titulo}' não encontrado no acervo.")
        return False

    def devolver(self, matricula, titulo):
        usuario = self.buscar_usuario(matricula)
        if not usuario:
            print(f"❌ Usuário {matricula} não encontrado.")
            return False

        for emp in usuario.emprestimos:
            item, data_emprestimo = emp
            if item.titulo.lower() == titulo.lower():
                dias = (datetime.now() - data_emprestimo).days
                if dias > 14:   # prazo de 14 dias
                    multa = item.calcular_multa(dias - 14)
                    print(f"⚠️  Atraso de {dias - 14} dias. Multa: R$ {multa:.2f}")
                else:
                    print(f"✅ Devolvido no prazo ({dias} dias).")

                item.devolver()
                usuario.emprestimos.remove(emp)
                return True

        print(f"❌ Usuário não possui '{titulo}' emprestado.")
        return False

    # --- Relatórios ---
    def relatorio_acervo(self):
        print(f"\n📋 Acervo da {self.nome}:")
        print(f"   Total: {len(self._acervo)} itens")
        disponiveis = len(self.listar_disponiveis())
        print(f"   Disponíveis: {disponiveis}")
        print(f"   Emprestados: {len(self._acervo) - disponiveis}")
        print()
        for item in self._acervo:
            print(f"   {item}")

    # --- Métodos mágicos ---
    def __len__(self):
        return len(self._acervo)

    def __contains__(self, titulo):
        return any(item.titulo.lower() == titulo.lower() for item in self._acervo)

    def __str__(self):
        return f"📚 {self.nome} — {len(self)} itens no acervo"
          