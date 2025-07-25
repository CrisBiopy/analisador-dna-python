#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador de Sequências de DNA - Interface Gráfica
Programa com GUI para análise básica de sequências de DNA a partir de arquivo de texto.

Autor: Cris Bulgakan
Data: 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os

class DNAAnalyzerGUI:
    def __init__(self, root):
        """
        Inicializa a interface gráfica do analisador de DNA.
        
        Args:
            root: Janela principal do tkinter
        """
        self.root = root
        self.root.title("Analisador de Sequências DNA")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variáveis
        self.arquivo_selecionado = tk.StringVar()
        self.sequencias = []
        
        self.criar_interface()
        
    def criar_interface(self):
        """
        Cria todos os elementos da interface gráfica.
        """
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração de redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="🧬 Analisador de Sequências DNA", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seção de seleção de arquivo
        arquivo_frame = ttk.LabelFrame(main_frame, text="Arquivo de Sequências", padding="10")
        arquivo_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        arquivo_frame.columnconfigure(1, weight=1)
        
        ttk.Label(arquivo_frame, text="Arquivo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.arquivo_entry = ttk.Entry(arquivo_frame, textvariable=self.arquivo_selecionado, 
                                      state="readonly", width=50)
        self.arquivo_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.btn_selecionar = ttk.Button(arquivo_frame, text="Selecionar Arquivo", 
                                        command=self.selecionar_arquivo)
        self.btn_selecionar.grid(row=0, column=2)
        
        # Botões de ação
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.btn_analisar = ttk.Button(botoes_frame, text="🔬 Analisar Sequências", 
                                      command=self.analisar_sequencias, state="disabled")
        self.btn_analisar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_limpar = ttk.Button(botoes_frame, text="🗑️ Limpar Resultados", 
                                    command=self.limpar_resultados)
        self.btn_limpar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.btn_salvar = ttk.Button(botoes_frame, text="💾 Salvar Resultados", 
                                    command=self.salvar_resultados, state="disabled")
        self.btn_salvar.pack(side=tk.LEFT)
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados da Análise", padding="10")
        resultados_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        resultados_frame.columnconfigure(0, weight=1)
        resultados_frame.rowconfigure(0, weight=1)
        
        self.texto_resultados = scrolledtext.ScrolledText(resultados_frame, width=80, height=20, 
                                                         font=("Consolas", 10))
        self.texto_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barra de status
        self.status_var = tk.StringVar(value="Selecione um arquivo para começar")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def selecionar_arquivo(self):
        """
        Abre o diálogo para seleção de arquivo.
        """
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo de sequências DNA",
            filetypes=[
                ("Arquivos de texto", "*.txt"),
                ("Arquivos FASTA", "*.fasta *.fa *.fas"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivo:
            self.arquivo_selecionado.set(arquivo)
            self.btn_analisar.config(state="normal")
            self.status_var.set(f"Arquivo selecionado: {os.path.basename(arquivo)}")
    
    def ler_arquivo(self, caminho_arquivo):
        """
        Lê o arquivo de sequências de DNA e retorna uma lista com as sequências.
        
        Args:
            caminho_arquivo (str): Caminho para o arquivo de entrada
            
        Returns:
            list: Lista de sequências de DNA (strings)
        """
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                sequencias = [linha.strip().upper() for linha in arquivo if linha.strip()]
                # Filtra linhas que começam com '>' (formato FASTA)
                sequencias = [seq for seq in sequencias if not seq.startswith('>')]
                return sequencias
        except Exception as e:
            raise Exception(f"Erro ao ler o arquivo: {str(e)}")
    
    def validar_sequencia(self, sequencia):
        """
        Valida se a sequência contém apenas bases válidas (A, T, C, G).
        
        Args:
            sequencia (str): Sequência de DNA para validar
            
        Returns:
            tuple: (bool, list) - (é_válida, caracteres_inválidos)
        """
        bases_validas = set('ATCG')
        caracteres_invalidos = []
        
        for char in sequencia:
            if char not in bases_validas:
                if char not in caracteres_invalidos:
                    caracteres_invalidos.append(char)
        
        eh_valida = len(caracteres_invalidos) == 0
        return eh_valida, caracteres_invalidos
    
    def analisar_sequencia(self, sequencia):
        """
        Analisa uma sequência de DNA e retorna estatísticas básicas.
        
        Args:
            sequencia (str): Sequência de DNA para analisar
            
        Returns:
            dict: Dicionário com as estatísticas da sequência
        """
        # Conta cada base
        contagem_a = sequencia.count('A')
        contagem_t = sequencia.count('T')
        contagem_c = sequencia.count('C')
        contagem_g = sequencia.count('G')
        
        # Calcula o comprimento total
        comprimento = len(sequencia)
        
        # Calcula o conteúdo GC (porcentagem de G e C)
        if comprimento > 0:
            gc_content = ((contagem_g + contagem_c) / comprimento) * 100
        else:
            gc_content = 0.0
        
        return {
            'sequencia': sequencia,
            'comprimento': comprimento,
            'A': contagem_a,
            'T': contagem_t,
            'C': contagem_c,
            'G': contagem_g,
            'gc_content': gc_content
        }
    
    def analisar_sequencias(self):
        """
        Analisa todas as sequências do arquivo selecionado.
        """
        if not self.arquivo_selecionado.get():
            messagebox.showerror("Erro", "Nenhum arquivo foi selecionado!")
            return
        
        try:
            # Limpa resultados anteriores
            self.texto_resultados.delete(1.0, tk.END)
            
            # Atualiza status
            self.status_var.set("Lendo arquivo...")
            self.root.update()
            
            # Lê o arquivo
            self.sequencias = self.ler_arquivo(self.arquivo_selecionado.get())
            
            if not self.sequencias:
                messagebox.showwarning("Aviso", "O arquivo está vazio ou não contém sequências válidas.")
                return
            
            # Atualiza status
            self.status_var.set(f"Analisando {len(self.sequencias)} sequências...")
            self.root.update()
            
            # Cabeçalho dos resultados
            resultado_texto = "=" * 60 + "\n"
            resultado_texto += "🧬 ANÁLISE DE SEQUÊNCIAS DE DNA\n"
            resultado_texto += "=" * 60 + "\n\n"
            
            resultado_texto += f"Arquivo: {os.path.basename(self.arquivo_selecionado.get())}\n"
            resultado_texto += f"Total de sequências encontradas: {len(self.sequencias)}\n\n"
            
            # Processa cada sequência
            sequencias_validas = 0
            sequencias_invalidas = 0
            total_bases = 0
            total_gc = 0
            
            for i, sequencia in enumerate(self.sequencias, 1):
                resultado_texto += f"📊 SEQUÊNCIA {i}:\n"
                resultado_texto += "-" * 40 + "\n"
                
                # Valida a sequência
                eh_valida, caracteres_invalidos = self.validar_sequencia(sequencia)
                
                if eh_valida:
                    # Analisa a sequência
                    resultado = self.analisar_sequencia(sequencia)
                    
                    # Formata a sequência para exibição (quebra em linhas de 60 caracteres)
                    seq_formatada = self.formatar_sequencia(resultado['sequencia'])
                    
                    resultado_texto += f"Sequência:\n{seq_formatada}\n\n"
                    resultado_texto += f"Comprimento: {resultado['comprimento']} bases\n"
                    resultado_texto += f"Composição: A={resultado['A']}, T={resultado['T']}, "
                    resultado_texto += f"C={resultado['C']}, G={resultado['G']}\n"
                    resultado_texto += f"Conteúdo GC: {resultado['gc_content']:.2f}%\n"
                    
                    sequencias_validas += 1
                    total_bases += resultado['comprimento']
                    total_gc += resultado['gc_content']
                    
                else:
                    resultado_texto += f"❌ SEQUÊNCIA INVÁLIDA!\n"
                    resultado_texto += f"Sequência: {sequencia}\n"
                    resultado_texto += f"Caracteres inválidos: {', '.join(caracteres_invalidos)}\n"
                    sequencias_invalidas += 1
                
                resultado_texto += "\n" + "=" * 60 + "\n\n"
            
            # Resumo estatístico
            if sequencias_validas > 0:
                gc_medio = total_gc / sequencias_validas
                resultado_texto += "📈 RESUMO ESTATÍSTICO:\n"
                resultado_texto += "-" * 40 + "\n"
                resultado_texto += f"Sequências válidas: {sequencias_validas}\n"
                resultado_texto += f"Sequências inválidas: {sequencias_invalidas}\n"
                resultado_texto += f"Total de bases analisadas: {total_bases:,}\n"
                resultado_texto += f"Conteúdo GC médio: {gc_medio:.2f}%\n"
            
            # Exibe os resultados
            self.texto_resultados.insert(1.0, resultado_texto)
            
            # Habilita o botão de salvar
            self.btn_salvar.config(state="normal")
            
            # Atualiza status
            self.status_var.set(f"Análise concluída! {sequencias_validas} sequências válidas, "
                               f"{sequencias_invalidas} inválidas")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante a análise:\n{str(e)}")
            self.status_var.set("Erro na análise")
    
    def formatar_sequencia(self, sequencia, largura=60):
        """
        Formata a sequência quebrando em linhas de tamanho específico.
        
        Args:
            sequencia (str): Sequência para formatar
            largura (int): Número de caracteres por linha
            
        Returns:
            str: Sequência formatada
        """
        linhas = []
        for i in range(0, len(sequencia), largura):
            linhas.append(sequencia[i:i+largura])
        return '\n'.join(linhas)
    
    def limpar_resultados(self):
        """
        Limpa a área de resultados.
        """
        self.texto_resultados.delete(1.0, tk.END)
        self.btn_salvar.config(state="disabled")
        self.status_var.set("Resultados limpos")
    
    def salvar_resultados(self):
        """
        Salva os resultados em um arquivo de texto.
        """
        if not self.texto_resultados.get(1.0, tk.END).strip():
            messagebox.showwarning("Aviso", "Não há resultados para salvar!")
            return
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar resultados",
            defaultextension=".txt",
            filetypes=[
                ("Arquivos de texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(self.texto_resultados.get(1.0, tk.END))
                
                messagebox.showinfo("Sucesso", f"Resultados salvos em:\n{arquivo}")
                self.status_var.set(f"Resultados salvos: {os.path.basename(arquivo)}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")

def main():
    """
    Função principal que inicializa a aplicação.
    """
    root = tk.Tk()
    app = DNAAnalyzerGUI(root)
    
    # Centraliza a janela na tela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()