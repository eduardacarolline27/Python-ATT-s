import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

# Constantes
DB_FILE = "agenda_medica.db"

#############################################
# MÓDULO DE GERENCIAMENTO DO BANCO DE DADOS #
#############################################

def conectar_bd():
    """Conecta ao banco de dados SQLite."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row # Retorna linhas como dicionários
        conn.execute("PRAGMA foreign_keys = ON") # Habilita chaves estrangeiras
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas(conn):
    """Cria as tabelas no banco de dados se não existirem."""
    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medico (
            id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especialidade TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS paciente (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            telefone TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS consulta (
            id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_medico INTEGER NOT NULL,
            id_paciente INTEGER NOT NULL,
            data_hora TEXT NOT NULL, -- Formato recomendado: YYYY-MM-DD HH:MM
            observacoes TEXT,
            FOREIGN KEY (id_medico) REFERENCES medico (id_medico) ON DELETE CASCADE,
            FOREIGN KEY (id_paciente) REFERENCES paciente (id_paciente) ON DELETE CASCADE
        );
        """)
        conn.commit()
        print("Tabelas criadas com sucesso (se não existiam).")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        cursor.close()

def inicializar_bd():
    """Inicializa o banco de dados: conecta e cria as tabelas."""
    # Verifica se o arquivo do banco de dados existe e tem tamanho maior que 0
    db_existe = os.path.exists(DB_FILE) and os.path.getsize(DB_FILE) > 0

    conn = conectar_bd()
    if conn:
        if not db_existe:
            print("Banco de dados não encontrado ou vazio. Criando tabelas...")
            criar_tabelas(conn)
        else:
            print("Banco de dados encontrado.")
        return conn
    return None

# --- Funções CRUD para Médicos ---

def adicionar_medico(conn, nome, especialidade):
    sql = 'INSERT INTO medico(nome, especialidade) VALUES(?,?)'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (nome, especialidade))
        conn.commit()
        print(f"Médico '{nome}' adicionado com sucesso.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao adicionar médico: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def listar_medicos(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM medico ORDER BY nome")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar médicos: {e}")
        return []
    finally:
        cursor.close()

def atualizar_medico(conn, id_medico, nome, especialidade):
    sql = 'UPDATE medico SET nome = ?, especialidade = ? WHERE id_medico = ?'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (nome, especialidade, id_medico))
        conn.commit()
        print(f"Médico ID {id_medico} atualizado com sucesso.")
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao atualizar médico: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def deletar_medico(conn, id_medico):
    sql = 'DELETE FROM medico WHERE id_medico = ?'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_medico,))
        conn.commit()
        print(f"Médico ID {id_medico} deletado com sucesso.")
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao deletar médico: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

# --- Funções CRUD para Pacientes ---

def adicionar_paciente(conn, nome, data_nascimento, telefone):
    sql = 'INSERT INTO paciente(nome, data_nascimento, telefone) VALUES(?,?,?)'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (nome, data_nascimento, telefone))
        conn.commit()
        print(f"Paciente '{nome}' adicionado com sucesso.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao adicionar paciente: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def listar_pacientes(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM paciente ORDER BY nome")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar pacientes: {e}")
        return []
    finally:
        cursor.close()

def atualizar_paciente(conn, id_paciente, nome, data_nascimento, telefone):
    sql = 'UPDATE paciente SET nome = ?, data_nascimento = ?, telefone = ? WHERE id_paciente = ?'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (nome, data_nascimento, telefone, id_paciente))
        conn.commit()
        print(f"Paciente ID {id_paciente} atualizado com sucesso.")
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao atualizar paciente: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def deletar_paciente(conn, id_paciente):
    sql = 'DELETE FROM paciente WHERE id_paciente = ?'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_paciente,))
        conn.commit()
        print(f"Paciente ID {id_paciente} deletado com sucesso.")
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao deletar paciente: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

# --- Funções CRUD para Consultas ---

def adicionar_consulta(conn, id_medico, id_paciente, data_hora, observacoes):
    sql = 'INSERT INTO consulta(id_medico, id_paciente, data_hora, observacoes) VALUES(?,?,?,?)'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_medico, id_paciente, data_hora, observacoes))
        conn.commit()
        print(f"Consulta agendada para {data_hora} com sucesso.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao agendar consulta: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def listar_consultas(conn):
    """Lista todas as consultas com nomes de médico e paciente."""
    sql = """
    SELECT
        c.id_consulta,
        c.data_hora,
        m.nome AS nome_medico,
        p.nome AS nome_paciente,
        c.observacoes,
        c.id_medico,
        c.id_paciente
    FROM consulta c
    JOIN medico m ON c.id_medico = m.id_medico
    JOIN paciente p ON c.id_paciente = p.id_paciente
    ORDER BY c.data_hora
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar consultas: {e}")
        return []
    finally:
        cursor.close()

def atualizar_consulta(conn, id_consulta, id_medico, id_paciente, data_hora, observacoes):
    sql = 'UPDATE consulta SET id_medico = ?, id_paciente = ?, data_hora = ?, observacoes = ? WHERE id_consulta = ?'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_medico, id_paciente, data_hora, observacoes, id_consulta))
        conn.commit()
        print(f"Consulta ID {id_consulta} atualizada com sucesso.")
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao atualizar consulta: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def deletar_consulta(conn, id_consulta):
    sql = 'DELETE FROM consulta WHERE id_consulta = ?'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (id_consulta,))
        conn.commit()
        print(f"Consulta ID {id_consulta} deletada com sucesso.")
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao deletar consulta: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

#############################
# MÓDULO DE INTERFACE AJUDA #
#############################

def mostrar_sobre():
    """Exibe a janela 'Sobre' com informações do projeto e integrantes."""
    integrantes = "Eduarda Carolline" # Nome fornecido pelo usuário
    titulo = "Agenda Médica"
    descricao = ("Aplicação para gerenciamento de médicos, pacientes e consultas.\n"
                 "Desenvolvida como parte do desafio de integração com interface gráfica e banco de dados.")

    messagebox.showinfo(
        f"Sobre - {titulo}",
        f"Título: {titulo}\n\n"
        f"Descrição: {descricao}\n\n"
        f"Integrantes: {integrantes}"
    )

#############################
# MÓDULO DE INTERFACE MÉDICO #
#############################

class TelaMedicos:
    def __init__(self, container, conn):
        self.container = container
        self.conn = conn
        self.frame = ttk.Frame(self.container)

        # --- Widgets --- #
        # Frame para o formulário
        form_frame = ttk.LabelFrame(self.frame, text="Dados do Médico")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Especialidade:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.especialidade_entry = ttk.Entry(form_frame, width=40)
        self.especialidade_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Frame para os botões
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ttk.Button(button_frame, text="Adicionar", command=self.adicionar_medico)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_medico)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Deletar", command=self.deletar_medico)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Limpar Campos", command=self.limpar_campos)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Frame para a Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar colunas da Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Especialidade"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Especialidade", text="Especialidade")

        # Ajustar largura das colunas
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nome", width=300)
        self.tree.column("Especialidade", width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar expansão da Treeview
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Vincular evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.item_selecionado)

        # Carregar dados iniciais
        self.carregar_medicos()

        # Adicionar o frame principal ao container
        self.frame.pack(fill=tk.BOTH, expand=True)

    def carregar_medicos(self):
        # Limpar Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Buscar dados no BD
        medicos = listar_medicos(self.conn)
        for medico in medicos:
            self.tree.insert("", tk.END, values=(medico["id_medico"], medico["nome"], medico["especialidade"]))

    def adicionar_medico(self):
        nome = self.nome_entry.get()
        especialidade = self.especialidade_entry.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do médico é obrigatório.")
            return

        if adicionar_medico(self.conn, nome, especialidade):
            messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!")
            self.limpar_campos()
            self.carregar_medicos()
        else:
            messagebox.showerror("Erro", "Falha ao adicionar médico.")

    def atualizar_medico(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um médico para atualizar.")
            return

        item = selected_item[0]
        id_medico = self.tree.item(item, "values")[0]
        nome = self.nome_entry.get()
        especialidade = self.especialidade_entry.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do médico é obrigatório.")
            return

        if atualizar_medico(self.conn, id_medico, nome, especialidade):
            messagebox.showinfo("Sucesso", "Médico atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_medicos()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar médico.")

    def deletar_medico(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um médico para deletar.")
            return

        item = selected_item[0]
        id_medico = self.tree.item(item, "values")[0]
        nome_medico = self.tree.item(item, "values")[1]

        confirm = messagebox.askyesno("Confirmar Deleção", f"Tem certeza que deseja deletar o médico \"{nome_medico}\"? Isso também deletará todas as consultas associadas a ele.")
        if confirm:
            if deletar_medico(self.conn, id_medico):
                messagebox.showinfo("Sucesso", "Médico deletado com sucesso!")
                self.limpar_campos()
                self.carregar_medicos()
            else:
                messagebox.showerror("Erro", "Falha ao deletar médico.")

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.especialidade_entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection()) # Desseleciona item na treeview

    def item_selecionado(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = selected_item[0]
        values = self.tree.item(item, "values")

        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, values[1])

        self.especialidade_entry.delete(0, tk.END)
        self.especialidade_entry.insert(0, values[2])

def abrir_tela_medicos(container, conn):
    # Limpa o container antes de adicionar a nova tela
    for widget in container.winfo_children():
        widget.destroy()
    # Cria a instância da tela
    TelaMedicos(container, conn)

###############################
# MÓDULO DE INTERFACE PACIENTE #
###############################

class TelaPacientes:
    def __init__(self, container, conn):
        self.container = container
        self.conn = conn
        self.frame = ttk.Frame(self.container)

        # --- Widgets --- #
        # Frame para o formulário
        form_frame = ttk.LabelFrame(self.frame, text="Dados do Paciente")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nome_entry = ttk.Entry(form_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Data Nasc.:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.data_nasc_entry = ttk.Entry(form_frame, width=20)
        self.data_nasc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(form_frame, text="(AAAA-MM-DD)").grid(row=1, column=2, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Telefone:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.telefone_entry = ttk.Entry(form_frame, width=20)
        self.telefone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Frame para os botões
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ttk.Button(button_frame, text="Adicionar", command=self.adicionar_paciente)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_paciente)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Deletar", command=self.deletar_paciente)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Limpar Campos", command=self.limpar_campos)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Frame para a Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar colunas da Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Data Nasc.", "Telefone"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data Nasc.", text="Data Nasc.")
        self.tree.heading("Telefone", text="Telefone")

        # Ajustar largura das colunas
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nome", width=300)
        self.tree.column("Data Nasc.", width=100, anchor=tk.CENTER)
        self.tree.column("Telefone", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar expansão da Treeview
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Vincular evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.item_selecionado)

        # Carregar dados iniciais
        self.carregar_pacientes()

        # Adicionar o frame principal ao container
        self.frame.pack(fill=tk.BOTH, expand=True)

    def carregar_pacientes(self):
        # Limpar Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Buscar dados no BD
        pacientes = listar_pacientes(self.conn)
        for paciente in pacientes:
            self.tree.insert("", tk.END, values=(paciente["id_paciente"], paciente["nome"], paciente["data_nascimento"], paciente["telefone"]))

    def adicionar_paciente(self):
        nome = self.nome_entry.get()
        data_nasc = self.data_nasc_entry.get()
        telefone = self.telefone_entry.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do paciente é obrigatório.")
            return
        # TODO: Adicionar validação para formato da data

        if adicionar_paciente(self.conn, nome, data_nasc, telefone):
            messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")
            self.limpar_campos()
            self.carregar_pacientes()
        else:
            messagebox.showerror("Erro", "Falha ao adicionar paciente.")

    def atualizar_paciente(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um paciente para atualizar.")
            return

        item = selected_item[0]
        id_paciente = self.tree.item(item, "values")[0]
        nome = self.nome_entry.get()
        data_nasc = self.data_nasc_entry.get()
        telefone = self.telefone_entry.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do paciente é obrigatório.")
            return
        # TODO: Adicionar validação para formato da data

        if atualizar_paciente(self.conn, id_paciente, nome, data_nasc, telefone):
            messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_pacientes()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar paciente.")

    def deletar_paciente(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um paciente para deletar.")
            return

        item = selected_item[0]
        id_paciente = self.tree.item(item, "values")[0]
        nome_paciente = self.tree.item(item, "values")[1]

        confirm = messagebox.askyesno("Confirmar Deleção", f"Tem certeza que deseja deletar o paciente \"{nome_paciente}\"? Isso também deletará todas as consultas associadas a ele.")
        if confirm:
            if deletar_paciente(self.conn, id_paciente):
                messagebox.showinfo("Sucesso", "Paciente deletado com sucesso!")
                self.limpar_campos()
                self.carregar_pacientes()
            else:
                messagebox.showerror("Erro", "Falha ao deletar paciente.")

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.data_nasc_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection()) # Desseleciona item na treeview

    def item_selecionado(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = selected_item[0]
        values = self.tree.item(item, "values")

        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, values[1])

        self.data_nasc_entry.delete(0, tk.END)
        self.data_nasc_entry.insert(0, values[2])

        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, values[3])

def abrir_tela_pacientes(container, conn):
    # Limpa o container antes de adicionar a nova tela
    for widget in container.winfo_children():
        widget.destroy()
    # Cria a instância da tela
    TelaPacientes(container, conn)

###############################
# MÓDULO DE INTERFACE CONSULTA #
###############################

class TelaConsultas:
    def __init__(self, container, conn):
        self.container = container
        self.conn = conn
        self.frame = ttk.Frame(self.container)

        # Dicionários para mapear nomes para IDs (para Comboboxes)
        self.medicos_map = {}
        self.pacientes_map = {}

        # --- Widgets --- #
        # Frame para o formulário
        form_frame = ttk.LabelFrame(self.frame, text="Agendar/Editar Consulta")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(form_frame, text="Médico:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.medico_combobox = ttk.Combobox(form_frame, state="readonly", width=38)
        self.medico_combobox.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.carregar_medicos_combobox()

        ttk.Label(form_frame, text="Paciente:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.paciente_combobox = ttk.Combobox(form_frame, state="readonly", width=38)
        self.paciente_combobox.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.carregar_pacientes_combobox()

        ttk.Label(form_frame, text="Data e Hora:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.data_hora_entry = ttk.Entry(form_frame, width=20)
        self.data_hora_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(form_frame, text="(AAAA-MM-DD HH:MM)").grid(row=2, column=2, padx=5, pady=5, sticky="w")

        ttk.Label(form_frame, text="Observações:").grid(row=3, column=0, padx=5, pady=5, sticky="nw")
        self.obs_text = tk.Text(form_frame, width=40, height=4)
        self.obs_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Frame para os botões
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ttk.Button(button_frame, text="Agendar", command=self.agendar_consulta)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ttk.Button(button_frame, text="Atualizar", command=self.atualizar_consulta)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Deletar", command=self.deletar_consulta)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Limpar Campos", command=self.limpar_campos)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Frame para a Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar colunas da Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Data/Hora", "Médico", "Paciente", "Obs"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data/Hora", text="Data/Hora")
        self.tree.heading("Médico", text="Médico")
        self.tree.heading("Paciente", text="Paciente")
        self.tree.heading("Obs", text="Observações")

        # Ajustar largura das colunas
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Data/Hora", width=120, anchor=tk.CENTER)
        self.tree.column("Médico", width=200)
        self.tree.column("Paciente", width=200)
        self.tree.column("Obs", width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar expansão da Treeview
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Vincular evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.item_selecionado)

        # Carregar dados iniciais
        self.carregar_consultas()

        # Adicionar o frame principal ao container
        self.frame.pack(fill=tk.BOTH, expand=True)

    def carregar_medicos_combobox(self):
        medicos = listar_medicos(self.conn)
        medico_nomes = []
        self.medicos_map.clear()
        for medico in medicos:
            nome_display = f"{medico['nome']} ({medico['especialidade']})" if medico['especialidade'] else medico['nome']
            self.medicos_map[nome_display] = medico['id_medico']
            medico_nomes.append(nome_display)
        self.medico_combobox['values'] = medico_nomes

    def carregar_pacientes_combobox(self):
        pacientes = listar_pacientes(self.conn)
        paciente_nomes = []
        self.pacientes_map.clear()
        for paciente in pacientes:
            self.pacientes_map[paciente['nome']] = paciente['id_paciente']
            paciente_nomes.append(paciente['nome'])
        self.paciente_combobox['values'] = paciente_nomes

    def carregar_consultas(self):
        # Limpar Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Buscar dados no BD (com JOIN)
        consultas = listar_consultas(self.conn)
        for consulta in consultas:
            self.tree.insert("", tk.END, values=(
                consulta["id_consulta"],
                consulta["data_hora"],
                consulta["nome_medico"],
                consulta["nome_paciente"],
                consulta["observacoes"]
            ))

    def validar_data_hora(self, data_hora_str):
        try:
            datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')
            return True
        except ValueError:
            messagebox.showerror("Erro de Formato", "Formato de Data/Hora inválido. Use AAAA-MM-DD HH:MM.")
            return False

    def agendar_consulta(self):
        medico_selecionado = self.medico_combobox.get()
        paciente_selecionado = self.paciente_combobox.get()
        data_hora = self.data_hora_entry.get()
        observacoes = self.obs_text.get("1.0", tk.END).strip()

        if not medico_selecionado or not paciente_selecionado or not data_hora:
            messagebox.showerror("Erro", "Médico, Paciente e Data/Hora são obrigatórios.")
            return

        if not self.validar_data_hora(data_hora):
            return

        id_medico = self.medicos_map.get(medico_selecionado)
        id_paciente = self.pacientes_map.get(paciente_selecionado)

        if not id_medico or not id_paciente:
             messagebox.showerror("Erro", "Médico ou Paciente inválido selecionado.") # Segurança extra
             return

        if adicionar_consulta(self.conn, id_medico, id_paciente, data_hora, observacoes):
            messagebox.showinfo("Sucesso", "Consulta agendada com sucesso!")
            self.limpar_campos()
            self.carregar_consultas()
            # Recarregar comboboxes caso um médico/paciente tenha sido adicionado em outra tela
            self.carregar_medicos_combobox()
            self.carregar_pacientes_combobox()
        else:
            messagebox.showerror("Erro", "Falha ao agendar consulta.")

    def atualizar_consulta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma consulta para atualizar.")
            return

        item = selected_item[0]
        id_consulta = self.tree.item(item, "values")[0]

        medico_selecionado = self.medico_combobox.get()
        paciente_selecionado = self.paciente_combobox.get()
        data_hora = self.data_hora_entry.get()
        observacoes = self.obs_text.get("1.0", tk.END).strip()

        if not medico_selecionado or not paciente_selecionado or not data_hora:
            messagebox.showerror("Erro", "Médico, Paciente e Data/Hora são obrigatórios.")
            return

        if not self.validar_data_hora(data_hora):
            return

        id_medico = self.medicos_map.get(medico_selecionado)
        id_paciente = self.pacientes_map.get(paciente_selecionado)

        if not id_medico or not id_paciente:
             messagebox.showerror("Erro", "Médico ou Paciente inválido selecionado.")
             return

        if atualizar_consulta(self.conn, id_consulta, id_medico, id_paciente, data_hora, observacoes):
            messagebox.showinfo("Sucesso", "Consulta atualizada com sucesso!")
            self.limpar_campos()
            self.carregar_consultas()
            self.carregar_medicos_combobox()
            self.carregar_pacientes_combobox()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar consulta.")

    def deletar_consulta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma consulta para deletar.")
            return

        item = selected_item[0]
        id_consulta = self.tree.item(item, "values")[0]
        data_hora_consulta = self.tree.item(item, "values")[1]

        confirm = messagebox.askyesno("Confirmar Deleção", f"Tem certeza que deseja deletar a consulta do dia {data_hora_consulta}?")
        if confirm:
            if deletar_consulta(self.conn, id_consulta):
                messagebox.showinfo("Sucesso", "Consulta deletada com sucesso!")
                self.limpar_campos()
                self.carregar_consultas()
            else:
                messagebox.showerror("Erro", "Falha ao deletar consulta.")

    def limpar_campos(self):
        self.medico_combobox.set('')
        self.paciente_combobox.set('')
        self.data_hora_entry.delete(0, tk.END)
        self.obs_text.delete("1.0", tk.END)
        self.tree.selection_remove(self.tree.selection()) # Desseleciona item na treeview

    def item_selecionado(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = selected_item[0]
        values = self.tree.item(item, "values") # ID, Data/Hora, Médico Nome, Paciente Nome, Obs

        # Buscar ID do médico e paciente correspondentes aos nomes
        # Isso é necessário para setar corretamente os comboboxes
        consulta_detalhes = None
        consultas_raw = listar_consultas(self.conn) # Pega dados com IDs
        for c in consultas_raw:
            if c['id_consulta'] == int(values[0]):
                consulta_detalhes = c
                break

        if not consulta_detalhes:
            print("Erro: Não foi possível encontrar detalhes da consulta selecionada.")
            self.limpar_campos()
            return

        # Encontrar a chave correta nos maps para setar os comboboxes
        medico_key = None
        for key, val_id in self.medicos_map.items():
            if val_id == consulta_detalhes['id_medico']:
                medico_key = key
                break

        paciente_key = None
        for key, val_id in self.pacientes_map.items():
            if val_id == consulta_detalhes['id_paciente']:
                paciente_key = key
                break

        self.medico_combobox.set(medico_key if medico_key else '')
        self.paciente_combobox.set(paciente_key if paciente_key else '')

        self.data_hora_entry.delete(0, tk.END)
        self.data_hora_entry.insert(0, values[1])

        self.obs_text.delete("1.0", tk.END)
        self.obs_text.insert("1.0", values[4])

def abrir_tela_consultas(container, conn):
    # Limpa o container antes de adicionar a nova tela
    for widget in container.winfo_children():
        widget.destroy()
    # Cria a instância da tela
    TelaConsultas(container, conn)

#############################
# APLICAÇÃO PRINCIPAL #
#############################

class App(tk.Tk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.title("Agenda Médica")
        # Definir um tamanho mínimo e permitir redimensionamento
        self.minsize(800, 600)
        # Centralizar a janela (opcional, pode variar dependendo do SO/WM)
        # self.eval('tk::PlaceWindow . center')

        # Container principal para as telas
        # Usar pack com fill e expand para ocupar o espaço disponível
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cria a barra de menus
        self.criar_menu()

        # Exibe uma tela inicial
        self.mostrar_tela_inicial()

    def criar_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Menu Cadastros
        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)
        # Usar as funções importadas dos módulos UI
        menu_cadastros.add_command(label="Médicos", command=lambda: abrir_tela_medicos(self.container, self.conn))
        menu_cadastros.add_command(label="Pacientes", command=lambda: abrir_tela_pacientes(self.container, self.conn))

        # Menu Agendamento
        menu_agendamento = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Agendamento", menu=menu_agendamento)
        menu_agendamento.add_command(label="Consultas", command=lambda: abrir_tela_consultas(self.container, self.conn))

        # Menu Ajuda
        menu_ajuda_menu = tk.Menu(menubar, tearoff=0) # Renomeado para evitar conflito
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda_menu)
        # Usar a função importada do módulo ui_ajuda
        menu_ajuda_menu.add_command(label="Sobre", command=mostrar_sobre)

    def mostrar_tela_inicial(self):
        """Mostra uma mensagem de boas-vindas no container."""
        # Limpa o container antes de adicionar a nova tela
        for widget in self.container.winfo_children():
            widget.destroy()
        label = ttk.Label(self.container, text="Bem-vindo à Agenda Médica!\nUse o menu superior para navegar.", font=("Arial", 14), justify=tk.CENTER)
        # Usar pack com expand para centralizar melhor
        label.pack(padx=20, pady=50, expand=True)

if __name__ == "__main__":
    print("Iniciando aplicação Agenda Médica...")
    conexao = inicializar_bd()
    if conexao:
        app = App(conexao)
        app.mainloop()
        # Fecha a conexão com o BD ao sair da aplicação
        conexao.close()
        print("Conexão com o banco de dados fechada.")
    else:
        print("Erro: Não foi possível conectar ao banco de dados. A aplicação não pode iniciar.")
        messagebox.showerror("Erro de Banco de Dados", "Não foi possível conectar ao banco de dados SQLite. Verifique o console para mais detalhes.")
