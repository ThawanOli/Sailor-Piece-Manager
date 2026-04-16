import customtkinter as ctk
import json
import os

# --- DICIONÁRIO DE TRADUÇÃO ---
TRADUCOES = {
    "Português": {
        "titulo": "Calculadora do Imperador",
        "lista_label": "Sets Salvos",
        "nome_set": "Nome do Set:",
        "materiais_label": "Materiais (Nome, Custo, Tenho):",
        "btn_calc": "Calcular Quantidade de Sets",
        "btn_salvar": "Salvar Base do Set",
        "btn_apagar": "Apagar Set",
        "placeholder_nome": "Ex: Set Cid v2",
        "resultado_limpo": "Resultado: --",
        "msg_salvo": "Template Salvo!",
        "msg_erro_formato": "Erro: Use Nome, Custo, Tenho",
        "msg_erro_num": "Erro: Use apenas números!",
        "msg_removido": "Set removido!",
        "instrucao": "Formato: Nome, Custo, Tenho"
    },
    "English": {
        "titulo": "Emperor's Calc",
        "lista_label": "Saved Sets",
        "nome_set": "Set Name:",
        "materiais_label": "Materials (Name, Cost, Owned):",
        "btn_calc": "Calculate Max Sets",
        "btn_salvar": "Save Set Base",
        "btn_apagar": "Delete Set",
        "placeholder_nome": "Ex: Cid v2 Set",
        "resultado_limpo": "Result: --",
        "msg_salvo": "Template Saved!",
        "msg_erro_formato": "Error: Use Name, Cost, Owned",
        "msg_erro_num": "Error: Use numbers only!",
        "msg_removido": "Set removed!",
        "instrucao": "Format: Name, Cost, Owned"
    }
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações de Janela
        self.title("Sailor Piece Manager | Dev: ThawanOli")
        self.geometry("850x680")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Dados e Estado
        self.idioma_atual = "Português"
        self.arquivo_salvo = "meus_sets.json"
        self.banco_de_dados = self.carregar_arquivo_disco()

        # Layout (Grid)
        self.grid_columnconfigure(0, weight=1) # Barra Lateral
        self.grid_columnconfigure(1, weight=3) # Área Principal

        # --- BARRA LATERAL ---
        self.frame_lista = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.frame_lista.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.btn_idioma = ctk.CTkSegmentedButton(self.frame_lista, values=["Português", "English"], 
                                                 command=self.mudar_idioma)
        self.btn_idioma.set("Português")
        self.btn_idioma.pack(pady=20, padx=10)

        self.label_lista = ctk.CTkLabel(self.frame_lista, text=TRADUCOES["Português"]["lista_label"], font=("Roboto", 16, "bold"))
        self.label_lista.pack(pady=5)

        self.scroll_lista = ctk.CTkScrollableFrame(self.frame_lista, width=200)
        self.scroll_lista.pack(pady=10, fill="both", expand=True, padx=5)

        # --- ÁREA PRINCIPAL ---
        self.frame_editor = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_editor.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.label_titulo = ctk.CTkLabel(self.frame_editor, text=TRADUCOES["Português"]["titulo"], font=("Roboto", 28, "bold"))
        self.label_titulo.pack(pady=(0, 20))

        self.label_nome_set = ctk.CTkLabel(self.frame_editor, text=TRADUCOES["Português"]["nome_set"])
        self.label_nome_set.pack(anchor="w", padx=40)
        self.entry_nome = ctk.CTkEntry(self.frame_editor, width=400, placeholder_text=TRADUCOES["Português"]["placeholder_nome"])
        self.entry_nome.pack(pady=5)

        self.label_corpo = ctk.CTkLabel(self.frame_editor, text=TRADUCOES["Português"]["materiais_label"])
        self.label_corpo.pack(anchor="w", padx=40, pady=(10, 0))
        self.txt_materiais = ctk.CTkTextbox(self.frame_editor, width=500, height=250, font=("Consolas", 14))
        self.txt_materiais.pack(pady=10)

        # Botões de Ação
        self.btn_calcular = ctk.CTkButton(self.frame_editor, text=TRADUCOES["Português"]["btn_calc"], command=self.calcular, fg_color="#1f6aa5", font=("Roboto", 14, "bold"))
        self.btn_calcular.pack(pady=10, fill="x", padx=100)

        self.frame_botoes_sec = ctk.CTkFrame(self.frame_editor, fg_color="transparent")
        self.frame_botoes_sec.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self.frame_botoes_sec, text=TRADUCOES["Português"]["btn_salvar"], command=self.salvar_set, fg_color="#2b8a3e", hover_color="#236b30")
        self.btn_salvar.grid(row=0, column=0, padx=5)

        self.btn_apagar = ctk.CTkButton(self.frame_botoes_sec, text=TRADUCOES["Português"]["btn_apagar"], 
                                        command=self.apagar_set, fg_color="#c92a2a", hover_color="#a61e1e")
        self.btn_apagar.grid(row=0, column=1, padx=5)

        self.label_resultado = ctk.CTkLabel(self.frame_editor, text=TRADUCOES["Português"]["resultado_limpo"], 
                                            font=("Roboto", 22, "bold"), text_color="#32a852")
        self.label_resultado.pack(pady=20)

        # Footer com crédito
        self.label_credito = ctk.CTkLabel(self.frame_editor, text="Developed by Thawan Oliveira | @ThawanOli ", font=("Roboto", 10,"italic"), text_color="gray")
        self.label_credito.pack(side="bottom", pady=(40,20))

        self.atualizar_lista_ui()

    # --- LÓGICA ---
    def carregar_arquivo_disco(self):
        if os.path.exists(self.arquivo_salvo):
            try:
                with open(self.arquivo_salvo, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return {}
        return {}

    def mudar_idioma(self, escolha):
        self.idioma_atual = escolha
        t = TRADUCOES[escolha]
        self.label_titulo.configure(text=t["titulo"])
        self.label_lista.configure(text=t["lista_label"])
        self.label_nome_set.configure(text=t["nome_set"])
        self.label_corpo.configure(text=t["materiais_label"])
        self.btn_calcular.configure(text=t["btn_calc"])
        self.btn_salvar.configure(text=t["btn_salvar"])
        self.btn_apagar.configure(text=t["btn_apagar"])
        self.entry_nome.configure(placeholder_text=t["placeholder_nome"])
        self.label_resultado.configure(text=t["resultado_limpo"])

    def salvar_set(self):
        nome = self.entry_nome.get().strip()
        conteudo = self.txt_materiais.get("0.0", "end").strip()
        t = TRADUCOES[self.idioma_atual]
        
        if nome and conteudo:
            linhas_template = []
            for linha in conteudo.split('\n'):
                if not linha.strip(): continue
                partes = linha.split(',')
                if len(partes) >= 2:
                    linhas_template.append(f"{partes[0].strip()}, {partes[1].strip()}, 0")
            
            self.banco_de_dados[nome] = "\n".join(linhas_template)
            with open(self.arquivo_salvo, "w", encoding="utf-8") as f:
                json.dump(self.banco_de_dados, f, indent=4)
            self.atualizar_lista_ui()
            self.label_resultado.configure(text=t["msg_salvo"], text_color="yellow")

    def apagar_set(self):
        nome = self.entry_nome.get().strip()
        t = TRADUCOES[self.idioma_atual]
        if nome in self.banco_de_dados:
            del self.banco_de_dados[nome]
            with open(self.arquivo_salvo, "w", encoding="utf-8") as f:
                json.dump(self.banco_de_dados, f, indent=4)
            self.entry_nome.delete(0, "end")
            self.txt_materiais.delete("0.0", "end")
            self.atualizar_lista_ui()
            self.label_resultado.configure(text=t["msg_removido"], text_color="orange")

    def atualizar_lista_ui(self):
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()
        for nome in sorted(self.banco_de_dados.keys()):
            btn = ctk.CTkButton(self.scroll_lista, text=nome, fg_color="#343a40",
                                command=lambda n=nome: self.carregar_set_especifico(n))
            btn.pack(pady=3, fill="x", padx=5)

    def carregar_set_especifico(self, nome):
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, nome)
        self.txt_materiais.delete("0.0", "end")
        self.txt_materiais.insert("0.0", self.banco_de_dados[nome])
        self.label_resultado.configure(text=TRADUCOES[self.idioma_atual]["resultado_limpo"], text_color="#32a852")

    def calcular(self):
        t = TRADUCOES[self.idioma_atual]
        conteudo = self.txt_materiais.get("0.0", "end").strip()
        linhas = conteudo.split('\n')
        possibilidades = []
        try:
            for linha in linhas:
                if not linha.strip(): continue
                partes = linha.split(',')
                if len(partes) < 3:
                    self.label_resultado.configure(text=t["msg_erro_formato"], text_color="red")
                    return
                custo = int(partes[1].strip())
                tenho = int(partes[2].strip())
                possibilidades.append(tenho // custo)
            
            if possibilidades:
                res = min(possibilidades)
                texto_res = f"Total: {res} Sets" if self.idioma_atual == "Português" else f"Total: {res} Sets"
                self.label_resultado.configure(text=texto_res, text_color="#32a852")
        except ValueError:
            self.label_resultado.configure(text=t["msg_erro_num"], text_color="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()